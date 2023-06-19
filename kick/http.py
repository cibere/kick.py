from __future__ import annotations

import asyncio
import json
import logging
from typing import TYPE_CHECKING, Any, Coroutine, TypeVar, Union, reveal_type

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

    def __init__(self, method: str, path: str, referrer: str = "/") -> None:
        self.path: str = path
        self.method: str = method
        self.url = self.BASE + self.path
        self.referrer = self.DOMAIN + referrer


class HTTPClient:
    def __init__(self, client: Client):
        self.__session: ClientSession = MISSING
        self.ws: ChatroomWebSocket = MISSING
        self.client = client

        self.token: str = MISSING
        self.xsrf_token: str = MISSING
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        self.cookie_url = "https://kick.com"

    async def close(self) -> None:
        LOGGER.info("Closing HTTP Client...")
        if self.__session is not MISSING:
            await self.__session.close()
        if self.ws is not MISSING:
            await self.ws.close()

    async def login(self, *, username: str, password: str) -> None:
        route = Route("POST", "/login")
        route.url = route.DOMAIN + "/login"
        data = {
            "email": username,
            "password": password,
        }
        data = await self.request(route, json=data)
        print(data)

    async def start(self) -> None:
        if self.__session is MISSING:
            self.__session = ClientSession()

        actual_ws = await self.__session.ws_connect(
            f"wss://ws-us2.pusher.com/app/eb1d5f283081a78b932c?protocol=7&client=js&version=7.6.0&flash=false"
        )
        self.ws = ChatroomWebSocket(actual_ws, http=self)
        self.client.dispatch("ready")
        print("dispatched ready")
        await self.ws.start()

    async def request(self, route: Route, **kwargs) -> Any:
        if self.__session is MISSING:
            self.__session = ClientSession()

        headers = kwargs.pop("headers", {})
        headers["Referrer"] = route.referrer
        headers["Connection"] = "keep-alive"
        headers["Alt-Used"] = "kick.com"
        headers["User-Agent"] = self.user_agent

        cookies = kwargs.pop("cookies", {})

        if self.xsrf_token:
            headers["X-XSRF-TOKEN"] = self.xsrf_token
            cookies["XSRF-TOKEN"] = self.xsrf_token
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
            cookies["kick_session"] = self.token

        url = route.url
        endpoint = f"/{route.method.split('/')[-1]}"

        if "json" in kwargs:
            headers["Content-Type"] = "application/json"

        res: ClientResponse | None = None
        data: str | dict | None = None
        # try:
        for current_try in range(3):
            LOGGER.debug(
                f"Making request to {url}. headers: {headers}, params: {kwargs.get('params', None)}, json: {kwargs.get('json', None)}"
            )

            res = await self.__session.request(
                route.method,
                f"http://localhost:9090/request?url={url}",
                headers=headers,
                cookies=cookies,
                **kwargs,
            )

            if res is not None:
                self.token = getattr(
                    res.cookies.get("kick_session", MISSING), "value", MISSING
                )
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
        # finally:
        #     print("finally triggered")
        #     if page is not None:
        #         print("Closing page...")
        #         await page.close()
        print("Done2")
        if res is not None and data is not None:
            txt = await error_or_text(data)

            if res.status >= 500:
                raise InternalKickException(txt)

            raise HTTPException(txt)

        raise RuntimeError(
            f"Unreachable situation occured in http handling. Res: {res}, data: {data}"
        )
        # raise RuntimeError("Unreachable situation occured in http handling")

    def send_message(self, chatroom: int, content: str) -> Response[MessageSentPayload]:
        # raise RuntimeError("This is broky")
        return self.request(
            Route(
                method="POST",
                path=f"/messages/send/{chatroom}",
            ),
            data={"content": content, "type": "message"},
        )

    def get_user(self, streamer: str) -> Response[UserPayload]:
        return self.request(
            Route(method="GET", path=f"/channels/{streamer}", referrer=f"/{streamer}")
        )

    def get_chatter(self, streamer: str, chatter: str) -> Response[ChatterPayload]:
        return self.request(
            Route(
                method="GET",
                path=f"/channels/{streamer}/users/{chatter}",
                referrer=f"https://kick.com/{streamer}",
            )
        )
