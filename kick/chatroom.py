from __future__ import annotations

import asyncio
import json
from datetime import datetime
from typing import TYPE_CHECKING

from aiohttp import ClientWebSocketResponse as WebSocketResponse

from .enums import ChatroomChatMode
from .message import Message
from .object import BaseDataclass

if TYPE_CHECKING:
    from .http import HTTPClient
    from .types.user import ChatroomPayload

__all__ = ("Chatroom",)


class ChatroomWebSocket:
    def __init__(self, ws: WebSocketResponse, *, client, chatroom_id):
        self.ws = ws
        self.client = client
        self.send_json = ws.send_json
        self.chatroom_id = chatroom_id
        self._receive_msgs_task: asyncio.Task | None = None

    async def poll_event(self) -> None:
        raw_msg = await self.ws.receive()
        msg = raw_msg.json()["data"]
        data = json.loads(msg)

        if data["type"] == "message":
            msg = Message(data=data)
            await self.client.dispatch("message", msg)

    async def _receive_msgs(self) -> None:
        while not self.ws.closed:
            await self.poll_event()

    async def connect(self, wait: bool = False) -> None:
        if wait is False:
            self._receive_msgs_task = asyncio.create_task(self._receive_msgs())
        await self.send_json(
            {
                "event": "pusher:subscribe",
                "data": {"auth": "", "channel": f"chatrooms.{self.chatroom_id}.v2"},
            }
        )
        if wait is True:
            await self._receive_msgs()


class Chatroom(BaseDataclass["ChatroomPayload"]):
    _created_at: datetime | None = None
    _updated_at: datetime | None = None
    _ws: ChatroomWebSocket | None = None
    http: HTTPClient

    @property
    def id(self) -> int:
        return self.__data["id"]

    @property
    def chatable_type(self) -> str:
        return self.__data["chatable_type"]

    @property
    def channel_id(self) -> int:
        return self.__data["channel_id"]

    @property
    def created_at(self) -> datetime:
        if self._created_at is None:
            self._created_at = datetime.fromisoformat(self.__data["created_at"])
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        if self._updated_at is None:
            self._updated_at = datetime.fromisoformat(self.__data["updated_at"])
        return self._updated_at

    @property
    def chat_mode(self) -> ChatroomChatMode:
        return ChatroomChatMode(self.__data["chat_mode"])

    @property
    def slowmode(self) -> bool:
        return self.__data["slow_mode"]

    @property
    def followers_mode(self) -> bool:
        return self.__data["followers_mode"]

    @property
    def subscribers_mode(self) -> bool:
        return self.__data["subscribers_mode"]

    @property
    def emotes_mode(self) -> bool:
        return self.__data["emotes_mode"]

    @property
    def message_interval(self) -> int:
        return self.__data["message_interval"]

    @property
    def following_min_duration(self) -> int:
        return self.__data["following_min_duration"]

    async def connect(self, wait: bool = False) -> None:
        self._ws = await self.http.connect_to_chatroom(self.id, wait)
