from __future__ import annotations

import asyncio
import json
import logging
from typing import TYPE_CHECKING, Any, Coroutine, TypeVar, Union

from aiohttp import ClientConnectionError, ClientResponse, ClientSession

from . import __version__
from .chatroom import ChatroomWebSocket
from .errors import (
    CloudflareBypassException,
    Forbidden,
    HTTPException,
    InternalKickException,
    LoginFailure,
    NotFound,
)
from .utils import MISSING

if TYPE_CHECKING:
    from types.emotes import EmotesPayload

    from typing_extensions import Self

    from .client import Client, Credentials
    from .types.chatroom import ChatroomBannedWordsPayload, ChatroomRulesPayload
    from .types.leaderboard import LeaderboardPayload
    from .types.message import FetchMessagesPayload, V1MessageSentPayload
    from .types.user import ChatterPayload, UserPayload
    from .types.videos import GetVideosPayload

    T = TypeVar("T")
    Response = Coroutine[Any, Any, T]


LOGGER = logging.getLogger(__name__)

NOTFOUND_SIGNATURE = """
class="w-64 lg:w-[526px]"
""".strip()


async def json_or_text(response: ClientResponse, /) -> Union[dict[str, Any], str]:
    text = await response.text()
    try:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
    except KeyError:
        pass

    return text


async def error_or_text(data: Union[dict, str]) -> str:
    if isinstance(data, dict):
        return data["error"]
    else:
        return data


class Route:
    DOMAIN: str = "https://kick.com"
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
        self.url = self.DOMAIN + path
        return self


class HTTPClient:
    def __init__(self, client: Client):
        self.__session: ClientSession = MISSING
        self.ws: ChatroomWebSocket = MISSING
        self.client = client

        self.token: str = MISSING
        self.xsrf_token: str = MISSING
        self.globally_locked: bool = False

        self.user_agent = f"Kick.py V{__version__} (github.com/cibere/kick.py)"

        self.bypass_port = client._options.get("bypass_port", 9090)
        self.whitelisted = client._options.get("whitelisted", False)

    async def close(self) -> None:
        LOGGER.info("Closing HTTP Client...")
        if self.__session is not MISSING:
            await self.__session.close()
        if self.ws is not MISSING:
            await self.ws.close()

    async def login(self, credentials: Credentials) -> None:
        LOGGER.info("Logging in using username and password")

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

    async def start(self) -> None:
        LOGGER.debug(
            f"Starting HTTP client. Whitelisted: {self.whitelisted}, Bypass Port: {self.bypass_port}"
        )
        if self.__session is MISSING:
            self.__session = ClientSession()

        actual_ws = await self.__session.ws_connect(
            f"wss://ws-us2.pusher.com/app/eb1d5f283081a78b932c?protocol=7&client=js&version=7.6.0&flash=false"
        )
        self.ws = ChatroomWebSocket(actual_ws, http=self)
        self.client.dispatch("ready")
        await self.ws.start()

    async def request(self, route: Route, **kwargs) -> Any:
        if self.__session is MISSING:
            self.__session = ClientSession()

        headers = kwargs.pop("headers", {})
        headers["User-Agent"] = self.user_agent
        headers["Accepts"] = "application/json"

        cookies = kwargs.pop("cookies", {})

        if self.xsrf_token:
            headers["X-XSRF-TOKEN"] = self.xsrf_token
            cookies["XSRF-TOKEN"] = self.xsrf_token
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        url = route.url
        endpoint = f"/{route.method.split('/')[-1]}"

        if "json" in kwargs:
            headers["Content-Type"] = "application/json"

        res: ClientResponse | None = None
        data: str | dict | None = None

        for current_try in range(3):
            while self.globally_locked is True:
                await asyncio.sleep(2)

            LOGGER.debug(
                f"Making request to {route.method} {url}. headers: {headers}, params: {kwargs.get('params', None)}, json: {kwargs.get('json', None)}"
            )
            try:
                res = await self.__session.request(
                    route.method,
                    url
                    if self.whitelisted is True
                    else f"http://localhost:{self.bypass_port}/request?url={url}",
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
                self.xsrf_token = getattr(
                    res.cookies.get("XSRF-TOKEN", MISSING), "value", MISSING
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
                        raise Forbidden()
                    case 404:
                        error = await error_or_text(data)
                        raise NotFound("Not Found")
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
