from __future__ import annotations

import asyncio
import json
import logging
from typing import TYPE_CHECKING, Any, Coroutine, TypeVar, Union

import pyppeteer
from aiohttp import ClientSession
from aiohttp import ClientWebSocketResponse as WebSocket
from pyppeteer.browser import Browser
from pyppeteer.network_manager import Response as BrowserResponse
from pyppeteer.page import Page as BrowserPage

from . import __version__
from .chatroom import ChatroomWebSocket
from .errors import Forbidden, HTTPException, InternalKickException, NotFound

if TYPE_CHECKING:
    from types.user import ChatterPayload, UserPayload

    T = TypeVar("T")
    Response = Coroutine[Any, Any, T]

LOGGER = logging.getLogger(__name__)

NOTFOUND_SIGNATURE = """
class="w-64 lg:w-[526px]"
""".strip()


async def json_or_text(response: BrowserResponse, /) -> Union[dict[str, Any], str]:
    text = await response.text()
    try:
        if response.headers["content-type"] == "application/json":
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

    def __init__(
        self,
        method: str,
        path: str,
    ) -> None:
        self.path: str = path
        self.method: str = method
        self.url = self.BASE + self.path


class HTTPClient:
    def __init__(self, token: str):
        self.__browser: Browser | None = None
        self.__session: ClientSession | None = None
        self.token: str = token

        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0"
        self.chatrooms: list[ChatroomWebSocket] = []

    async def close(self) -> None:
        print("Closing HTTPClient...")
        if self.__browser is not None:
            await self.__browser.close()
        if self.__session is not None:
            for chatroom in self.chatrooms:
                await chatroom.ws.close()
            await self.__session.close()

    async def connect_to_chatroom(
        self, chatroom_id: int, wait: bool = False
    ) -> ChatroomWebSocket:
        ws = await self.create_ws(
            f"wss://ws-us2.pusher.com/app/eb1d5f283081a78b932c?protocol=7&client=js&version=7.6.0&flash=false"
        )
        chatroom = ChatroomWebSocket(ws, client=self, chatroom_id=chatroom_id)
        await chatroom.connect(wait)
        self.chatrooms.append(chatroom)
        return chatroom

    async def create_ws(self, url: str, **kwargs) -> WebSocket:
        if self.__session is None:
            self.__session = ClientSession()
        return await self.__session.ws_connect(url, **kwargs)

    async def request(self, route: Route, **kwargs) -> Any:
        if self.__browser is None:
            self.__browser = await pyppeteer.launch()

        headers = kwargs.pop("headers", {})
        headers["User-Agent"] = self.user_agent
        headers["Accept"] = "application/json"
        headers["Authorization"] = f"Bearer {self.token}"
        headers["Connection"] = "keep-alive"
        url = route.url
        endpoint = f"/{route.method.split('/')[-1]}"

        if "json" in kwargs:
            headers["Content-Type"] = "application/json"

        res: BrowserResponse | None = None
        data: str | dict | None = None
        page: BrowserPage | None = None
        try:
            for current_try in range(3):
                LOGGER.debug(
                    f"Making request to {url}. headers: {headers}, params: {kwargs.get('params', None)}, json: {kwargs.get('json', None)}"
                )
                page = await self.__browser.newPage()
                await page.setExtraHTTPHeaders(headers)
                res = await page.goto(url)
                if res is not None:
                    data = await json_or_text(res)

                    LOGGER.debug(
                        f"Received Response w/ code {res.status}. headers: {res.headers}, data: {data}"
                    )
                    if NOTFOUND_SIGNATURE in data:
                        error = await error_or_text(data)
                        raise NotFound(error)

                    if 300 > res.status >= 200:
                        return data
                    match res.status:
                        case 400:
                            error = await error_or_text(data)
                            raise HTTPException(error)
                        case 403:
                            error = await error_or_text(data)
                            raise Forbidden(error)
                        case 404:
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
        finally:
            if page is not None:
                await page.close()

        if res is not None and data is not None:
            txt = await error_or_text(data)

            if res.status >= 500:
                raise InternalKickException(txt)

            raise HTTPException(txt)

        raise RuntimeError("Unreachable situation occured in http handling")

    def send_message(self, chatroom: int, content: str) -> Response:
        return self.request(
            Route(method="POST", path=f"/messages/send/{chatroom}"),
            json={"content": content, "type": "message"},
        )

    def get_user(self, streamer: str) -> Response[UserPayload]:
        return self.request(Route(method="GET", path=f"/channels/{streamer}"))

    def get_user_chatroom_info(
        self, streamer: str, chatter: str
    ) -> Response[ChatterPayload]:
        return self.request(
            Route(method="GET", path=f"/channels/{streamer}/users/{chatter}")
        )
