from __future__ import annotations

import asyncio
import json
import logging
from typing import TYPE_CHECKING, Any, Coroutine, TypeVar, Union

from aiohttp import ClientResponse, ClientSession

from . import __version__
from .chatroom import ChatroomWebSocket
from .errors import (
    Forbidden,
    HTTPException,
    InternalKickException,
    LoginFailure,
    NotFound,
)
from .utils import MISSING

if TYPE_CHECKING:
    from .client import Client
    from .types.message import MessageSentPayload
    from .types.user import ChatterPayload, UserPayload

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


class HTTPClient:
    def __init__(self, client: Client):
        self.__session: ClientSession = MISSING
        self.ws: ChatroomWebSocket = MISSING
        self.client = client

        self.token: str = MISSING
        self.xsrf_token: str = MISSING

        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

        self.bypass_port = client._options.get("bypass_port", 9090)
        self.whitelisted = client._options.get("whitelisted", False)

    async def close(self) -> None:
        LOGGER.info("Closing HTTP Client...")
        if self.__session is not MISSING:
            await self.__session.close()
        if self.ws is not MISSING:
            await self.ws.close()

    async def login(
        self, *, username: str, password: str, one_time_password: str | None
    ) -> None:
        LOGGER.info("Logging in using username and password")

        # Mobile login method is used here since more is known about
        # how that works compared to the desktop version.
        # As for compatibility, there is no known endpoints that
        # a mobile token can not authorize at.

        token_route = Route("GET", "")
        token_route.url = token_route.DOMAIN + "/kick-token-provider"
        token_provider = await self.request(token_route)

        with open("token.json", "w") as f:
            json.dump(token_provider, f, indent=4)

        route = Route("POST", "")
        route.url = route.DOMAIN + "/mobile/login"

        data = {
            "email": username,
            "password": password,
            "isMobileRequest": True,
            token_provider["nameFieldName"]: "",
            token_provider["validFromFieldName"]: token_provider["encryptedValidFrom"],
        }
        if one_time_password is not None:
            data["one_time_password"] = one_time_password

        res = await self.request(route, json=data)
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
            LOGGER.debug(
                f"Making request to {route.method} {url}. headers: {headers}, params: {kwargs.get('params', None)}, json: {kwargs.get('json', None)}"
            )

            res = await self.__session.request(
                route.method,
                f"http://localhost:{self.bypass_port}/request?url={url}"
                if self.whitelisted is False
                else url,
                headers=headers,
                cookies=cookies,
                **kwargs,
            )

            if res is not None:
                self.xsrf_token = getattr(
                    res.cookies.get("XSRF-TOKEN", MISSING), "value", MISSING
                )

                data = await json_or_text(res)

                if 300 > res.status >= 200:
                    return data

                match res.status:
                    case 400:
                        error = await error_or_text(data)
                        raise HTTPException(error)
                    case 403:
                        print(data)
                        raise Forbidden()
                    case 404:
                        print("404")
                        error = await error_or_text(data)
                        raise NotFound(error)
                    case 429:
                        LOGGER.warning(
                            "We have been ratelimited. Waiting five seconds before trying again...",
                            endpoint,
                        )
                        await asyncio.sleep(5)
                        return await self.request(route)
                    case 500:
                        time = 2 * current_try

                        LOGGER.warning(
                            "API returned a 500 status code at '%s'. Retrying in %s seconds",
                            endpoint,
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

            raise HTTPException(txt)

        raise RuntimeError("Unreachable situation occured in http handling")

    def send_message(self, chatroom: int, content: str) -> Response[MessageSentPayload]:
        raise RuntimeError("This is broky")
        return self.request(
            Route(
                method="POST",
                path=f"/messages/send/{chatroom}",
            ),
            data={"content": content, "type": "message"},
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
