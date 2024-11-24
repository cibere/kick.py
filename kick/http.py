from __future__ import annotations

import asyncio
import json
import logging
from typing import TYPE_CHECKING, Any, Coroutine, Optional, TypeVar, Union

from aiohttp import ClientConnectionError, ClientResponse, ClientSession

from . import __version__
from .errors import (
    CloudflareBypassException,
    Forbidden,
    HTTPException,
    InternalKickException,
    LoginFailure,
    NotFound,
)
from .utils import MISSING
from .ws import PusherWebSocket

if TYPE_CHECKING:
    from types.emotes import EmotesPayload

    from typing_extensions import Self

    from .client import Client, Credentials
    from .types.chatroom import (
        BanChatterPayload,
        ChatroomBannedWordsPayload,
        ChatroomRulesPayload,
        CreatePollPayload,
        DeletePollPayload,
        EditChatroomSettingsPayload,
        GetBannedUsersPayload,
        UnbanChatterPayload,
    )
    from .types.leaderboard import LeaderboardPayload
    from .types.message import (
        FetchMessagesPayload,
        MessagePayload,
        ReplyOriginalMessage,
        ReplyOriginalSender,
        V1MessageSentPayload,
    )
    from .types.user import (
        ChatterPayload,
        ClientUserPayload,
        UserPayload,
        StreamInfoPayload,
        DestinationInfoPayload,
    )
    from .types.videos import GetVideosPayload
    from .types.search import CategorySearchResponse

    T = TypeVar("T")
    Response = Coroutine[Any, Any, T]


LOGGER = logging.getLogger(__name__)

NOTFOUND_SIGNATURE = """
class="w-64 lg:w-[526px]"
""".strip()


async def json_or_text(response: ClientResponse, /) -> Union[dict[str, Any], str]:
    text = await response.text()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    except KeyError:
        pass

    return text


async def error_or_text(data: Union[dict, str]) -> str:
    if isinstance(data, dict):
        if "status" in data:
            return data["status"]["message"]
        elif "error" in data:
            return data["error"]
        elif "message" in data:
            return data["message"]
    return f"{data}"


async def error_or_nothing(data: Union[dict, str]) -> str:
    if isinstance(data, dict):
        return await error_or_text(data)
    else:
        return ""


class Route:
    DOMAIN: str = "https://kick.com"
    SEARCH_DOMAIN: str = "https://search.kick.com"
    BASE: str = f"{DOMAIN}/api/v2"

    def __init__(self, method: str, path: str) -> None:
        self.path: str = path
        self.method: str = method
        self.url = self.BASE + self.path

    @classmethod
    def root(cls, method: str, path: str) -> Self:
        self = cls.__new__(cls)
        self.path = path
        self.method = method
        self.url = cls.DOMAIN + path
        return self

    @classmethod
    def search(cls, method: str, path: str) -> Self:
        self = cls.__new__(cls)
        self.path = path
        self.method = method
        self.url = cls.SEARCH_DOMAIN + path
        return self


class HTTPClient:
    def __init__(self, client: Client):
        self.__session: ClientSession = MISSING
        self.ws: PusherWebSocket = MISSING
        self.client = client

        self.token: str = MISSING
        self.xsrf_token: str = MISSING
        self.globally_locked: bool = False
        self.__regex_token_task: asyncio.Task | None = None
        self._credentials: Credentials | None = None

        self.user_agent = f"Kick.py V{__version__} (github.com/cibere/kick.py)"

        self.bypass_port = client._options.get("bypass_port", 9090)
        self.bypass_host = client._options.get("bypass_host", "http://localhost")
        self.whitelisted = client._options.get("whitelisted", False)

    async def regen_token_coro(self) -> None:
        await asyncio.sleep(2419200)  # 28 days just to be safe
        if self._credentials:
            LOGGER.info("Attempting to renew token")
            await self.client.login(self._credentials)

    async def close(self) -> None:
        LOGGER.info("Closing HTTP Client...")
        if self.__session is not MISSING:
            await self.__session.close()
        if self.ws is not MISSING:
            await self.ws.close()

    async def login(self, credentials: Credentials) -> None:
        self._credentials = credentials

        LOGGER.info(
            f"Logging in using {'username' if credentials.username_was_provided else 'email'} and password"
        )

        # Mobile login method is used here since more is known about
        # how that works compared to the desktop version.
        # As for compatibility, there is no known endpoints that
        # a mobile token can not authorize at.

        token_route = Route.root("GET", "/kick-token-provider")
        token_provider = await self.request(token_route)

        route = Route.root("POST", "/mobile/login")

        data = {
            "email": credentials.email,
            "password": credentials.password,
            "isMobileRequest": True,
            token_provider["nameFieldName"]: "",
            token_provider["validFromFieldName"]: token_provider["encryptedValidFrom"],
        }
        if credentials.one_time_password is not None:
            data["one_time_password"] = credentials.one_time_password

        res = await self.request(route, json=data)

        if isinstance(res, str):
            raise NotFound("Kick 404'd on login page")

        if res["2fa_required"] is True:
            two_fa_code = input(
                "[WARNING] 2FA is enabled. Either disable it or give a 2fa code.\n> "
            )
            if not two_fa_code:
                raise LoginFailure("2FA is enabled.")
            else:
                data["one_time_password"] = two_fa_code
                res = await self.request(route, json=data)
                if res["2fa_required"] is True:
                    raise LoginFailure("2FA is enabled.")

        if "message" in res.keys():
            raise LoginFailure(res["message"])

        self.token = res["token"]
        LOGGER.info("Successfully logged in")
        self.__regex_token_task = asyncio.create_task(
            self.regen_token_coro(), name="Regen-Token"
        )

    async def start(self) -> None:
        LOGGER.debug(
            f"Starting HTTP client. Whitelisted: {self.whitelisted}, Bypass Port: {self.bypass_port}"
        )
        if self.__session is MISSING:
            self.__session = ClientSession()

        actual_ws = await self.__session.ws_connect(
            f"wss://ws-us2.pusher.com/app/eb1d5f283081a78b932c?protocol=7&client=js&version=7.6.0&flash=false"
        )
        self.ws = PusherWebSocket(actual_ws, http=self)
        self.client.dispatch("ready")
        await self.ws.start()

    async def request(self, route: Route, **kwargs) -> Any:
        if self.__session is MISSING:
            self.__session = ClientSession()

        print(route.url)
        headers = kwargs.pop("headers", {})
        headers["User-Agent"] = self.user_agent
        headers["Accepts"] = "application/json"
        headers["X-TYPESENSE-API-KEY"] = "nXIMW0iEN6sMujFYjFuhdrSwVow3pDQu"

        cookies = kwargs.pop("cookies", {})

        if self.xsrf_token:
            headers["X-XSRF-TOKEN"] = self.xsrf_token
            cookies["XSRF-TOKEN"] = self.xsrf_token
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        url = route.url

        if "json" in kwargs:
            headers["Content-Type"] = "application/json"

        res: ClientResponse | None = None
        data: str | dict | None = None

        for current_try in range(3):
            while self.globally_locked is True:
                await asyncio.sleep(2)

            # Handle URL construction
            from urllib.parse import quote
            final_url = url
            
            if 'params' in kwargs:
                from urllib.parse import urlencode
                params = kwargs['params']
                params_str = urlencode(params, quote_via=quote)
                final_url = f"{url}?{params_str}"
                
            if not self.whitelisted:
                final_url = f"{self.bypass_host}:{self.bypass_port}/request?url={quote(final_url)}"
                
            LOGGER.debug(f"Using {'bypass' if not self.whitelisted else 'direct'} URL: {final_url}")
            
            # Remove params from kwargs if we're using bypass to prevent duplication
            if not self.whitelisted and kwargs.get('_bypass_params'):
                kwargs.pop('params', None)
            kwargs.pop('_bypass_params', None)
            
            
            LOGGER.debug(
                f"Making request to {route.method} {final_url}. headers: {headers}, params: {kwargs.get('params', None)}, json: {kwargs.get('json', None)}"
            )
            try:
                res = await self.__session.request(
                    route.method,
                    (
                        url
                        if self.whitelisted is True
                        else f"{self.bypass_host}:{self.bypass_port}/request?url={url}"
                    ),
                    headers=headers,
                    cookies=cookies,
                    **kwargs,
                )
            except ClientConnectionError:
                if self.whitelisted is True:
                    raise InternalKickException("Could Not Connect To Kick") from None
                else:
                    raise CloudflareBypassException(
                        "Could Not Connect To Bypass Script"
                    ) from None

            if res is not None:
                self.xsrf_token = str(
                    getattr(res.cookies.get("XSRF-TOKEN", MISSING), "value", MISSING)
                )

                data = await json_or_text(res)

                if res.status == 429:
                    self.globally_locked = True
                    LOGGER.warning(
                        f"We have been ratelimited at {route.method} {route.url}. Waiting five seconds before trying again...",
                    )

                    await asyncio.sleep(5)
                    return await self.request(route)
                else:
                    self.globally_locked = False

                if 300 > res.status >= 200:
                    return data

                match res.status:
                    case 400:
                        error = await error_or_text(data)
                        raise HTTPException(error, res.status)
                    case 403:
                        raise Forbidden(await error_or_nothing(data))
                    case 404:
                        error = await error_or_nothing(data)
                        raise NotFound(error or "Not Found")
                    case 500:
                        time = 2 * current_try

                        LOGGER.warning(
                            f"API returned a 500 status code at {route.method} {route.url}. Retrying in {time} seconds",
                        )
                        await asyncio.sleep(time)
                        continue
                    case 502:
                        txt = await error_or_text(data)
                        raise InternalKickException(txt)
                    case other:
                        raise RuntimeError(f"Unknown status reached: {other}")

        if res is not None and data is not None:
            txt = await error_or_text(data)

            if res.status >= 500:
                raise InternalKickException(txt)

            raise HTTPException(txt, res.status)

        raise RuntimeError("Unreachable situation occured in http handling")

    def send_message(
        self, chatroom: int, content: str
    ) -> Response[V1MessageSentPayload]:
        # We use the V1 api here since I havn't gotten it to work with V2.
        # Unfortunatly V1 only returns a confirmation, and not the message (unlike V2)

        route = Route.root("POST", "/api/v1/chat-messages")
        return self.request(
            route,
            data={"message": content, "chatroom_id": chatroom},
        )

    def delete_message(self, chatroom: int, message_id: str) -> Response[Any]:
        # Kick keeps 500ing on this, so not sure what to expect from it
        return self.request(
            Route("DELETE", f"/chatrooms/{chatroom}/messages/{message_id}")
        )

    def get_user(self, streamer: str) -> Response[UserPayload]:
        return self.request(Route(method="GET", path=f"/channels/{streamer}"))

    def get_chatter(self, streamer: str, chatter: str) -> Response[ChatterPayload]:
        return self.request(
            Route(
                method="GET",
                path=f"/channels/{streamer}/users/{chatter}",
            )
        )

    def get_messages(self, chatroom: int) -> Response[FetchMessagesPayload]:
        return self.request(Route("GET", f"/channels/{chatroom}/messages"))

    def get_chatroom_rules(self, streamer: str) -> Response[ChatroomRulesPayload]:
        return self.request(Route("GET", f"/channels/{streamer}/chatroom/rules"))

    def get_streamer_videos(self, streamer: str) -> Response[GetVideosPayload]:
        return self.request(Route("GET", f"/channels/{streamer}/videos"))

    def get_emotes(self, streamer: str) -> Response[EmotesPayload]:
        return self.request(Route.root("GET", f"/emotes/{streamer}"))

    def get_channels_banned_words(
        self, streamer: str
    ) -> Response[ChatroomBannedWordsPayload]:
        return self.request(Route("GET", f"/channels/{streamer}/chatroom/banned-words"))

    def get_channel_gift_leaderboard(
        self, streamer: str
    ) -> Response[LeaderboardPayload]:
        return self.request(Route.root("GET", f"/channels/{streamer}/leaderboards"))

    def get_channel_bans(self, streamer: str) -> Response[GetBannedUsersPayload]:
        """
        Requires Mod
        """

        return self.request(Route("GET", f"/channels/{streamer}/bans"))

    def unban_user(self, streamer: str, chatter: str) -> Response[UnbanChatterPayload]:
        return self.request(Route("DELETE", f"/channels/{streamer}/bans/{chatter}"))

    def timeout_chatter(
        self, streamer: str, chatter: str, reason: str, duration: int
    ) -> Response[BanChatterPayload]:
        return self.request(
            Route("POST", f"/channels/{streamer}/bans"),
            json={
                "banned_username": chatter,
                "permanent": False,
                "reason": reason,
                "duration": duration,
            },
        )

    def ban_chatter(
        self, streamer: str, chatter: str, reason: str
    ) -> Response[BanChatterPayload]:
        return self.request(
            Route("POST", f"/channels/{streamer}/bans"),
            json={
                "banned_username": chatter,
                "permanent": True,
                "reason": reason,
            },
        )

    def create_poll(
        self,
        streamer: str,
        duration: int,
        options: list[str],
        result_display_duration: int,
        title: str,
    ) -> Response[CreatePollPayload]:
        """
        Durations are in seconds
        """

        return self.request(
            Route("POST", f"/channels/{streamer}/polls"),
            json={
                "duration": duration,
                "options": options,
                "result_display_duration": result_display_duration,
                "title": title,
            },
        )

    def delete_poll(self, streamer: str) -> Response[DeletePollPayload]:
        return self.request(Route("DELETE", f"/channels/{streamer}/polls"))

    def vote_for_poll(self, streamer: str, option: int) -> Response[CreatePollPayload]:
        return self.request(
            Route("POST", f"/channels/{streamer}/polls/vote"),
            json={"id": option},
        )

    def get_poll(self, streamer: str) -> Response[CreatePollPayload]:
        return self.request(
            Route("GET", f"/channels/{streamer}/polls"),
        )

    def edit_chatroom(
        self,
        streamer: str,
        followers_only_mode: Optional[bool] = None,
        emotes_only_mode: Optional[bool] = None,
        subscribers_only_mode: Optional[bool] = None,
        slow_mode_enabled: Optional[bool] = None,
        slow_mode_interval: Optional[int] = None,
        following_min_duration: Optional[int] = None,
    ) -> Response[EditChatroomSettingsPayload]:
        payload = {}

        if followers_only_mode is not None:
            payload["followers_mode"] = followers_only_mode

        if emotes_only_mode is not None:
            payload["emotes_mode"] = emotes_only_mode

        if subscribers_only_mode is not None:
            payload["subscribers_mode"] = subscribers_only_mode

        if slow_mode_enabled is not None:
            payload["slow_mode"] = slow_mode_enabled
            if slow_mode_enabled and slow_mode_interval is not None:
                payload["message_interval"] = slow_mode_interval

        if following_min_duration is not None:
            payload["following_min_duration "] = following_min_duration

        if not payload:
            raise ValueError("No valid parameters provided for chatroom editing.")

        return self.request(
            Route("PUT", f"/channels/{streamer}/chatroom"),
            json=payload,
        )

    def reply_to_message(
        self,
        chatroom: int,
        content: str,
        original_message: ReplyOriginalMessage,
        original_sender: ReplyOriginalSender,
    ) -> Response[MessagePayload]:
        return self.request(
            Route("POST", f"/messages/send/{chatroom}"),
            json={
                "content": content,
                "metadata": {
                    "original_message": original_message,
                    "original_sender": original_sender,
                },
                "type": "reply",
            },
        )

    def get_me(self) -> Response[ClientUserPayload]:
        return self.request(Route.root("GET", "/api/v1/user"))

    def set_stream_info(self, info) -> Response[StreamInfoPayload]:
       return self.request(Route.root("PUT", "/stream/info"), json=info) 

    def search_categories(self, query: str) -> Response[CategorySearchResponse]:
        """Search for categories/games on Kick"""
        params = {
            "query_by": "name,slug",  # Specify fields to search in
            "q": query,
            "collections": "subcategory",
            "preset": "category_list"
        }
        return self.request(
            Route.search("GET", "/collections/subcategory_index/documents/search"),
            params=params,
            _bypass_params=True  # Flag to prevent param duplication
        )

    def get_stream_destination_url_and_key(self) -> Response[DestinationInfoPayload]:
        """Gets the authenticated user's stream URL and key.

        Returns
        -------
        StreamURLKeyPayload
            The stream URL and key information containing the publish URL and token
        """
        return self.request(Route.root("GET", "/stream/publish_token"))

    async def get_asset(self, url: str) -> bytes:
        if self.__session is MISSING:
            self.__session = ClientSession()

        res = await self.__session.request("GET", url)
        match res.status:
            case 200:
                return await res.read()
            case 403:
                raise Forbidden()
            case 404:
                raise NotFound("Asset Not Found")
            case 500:
                data = await json_or_text(res)
                error = await error_or_text(data)
                raise InternalKickException(error)
            case other:
                raise HTTPException(await res.text(), other)
