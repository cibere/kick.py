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
    def __init__(self, ws: WebSocketResponse, *, http: HTTPClient):
        self.ws = ws
        self.http = http
        self.send_json = ws.send_json
        self.close = ws.close
        self._receive_msgs_task: asyncio.Task | None = None

    async def poll_event(self) -> None:
        raw_msg = await self.ws.receive()
        msg = raw_msg.json()["data"]
        data = json.loads(msg)

        if data.get("type") == "message":
            msg = Message(data=data)
            self.http.client.dispatch("message", msg)

    async def start(self) -> None:
        while not self.ws.closed:
            await self.poll_event()

    async def subscribe(self, chatroom_id: int) -> None:
        await self.send_json(
            {
                "event": "pusher:subscribe",
                "data": {"auth": "", "channel": f"chatrooms.{chatroom_id}.v2"},
            }
        )


class Chatroom(BaseDataclass["ChatroomPayload"]):
    _created_at: datetime | None = None
    _updated_at: datetime | None = None
    _ws: ChatroomWebSocket | None = None
    http: HTTPClient

    @property
    def id(self) -> int:
        return self._data["id"]

    @property
    def chatable_type(self) -> str:
        return self._data["chatable_type"]

    @property
    def created_at(self) -> datetime:
        if self._created_at is None:
            self._created_at = datetime.fromisoformat(self._data["created_at"])
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        if self._updated_at is None:
            self._updated_at = datetime.fromisoformat(self._data["updated_at"])
        return self._updated_at

    @property
    def chat_mode(self) -> ChatroomChatMode:
        return ChatroomChatMode(self._data["chat_mode"])

    @property
    def slowmode(self) -> bool:
        return self._data["slow_mode"]

    @property
    def followers_mode(self) -> bool:
        return self._data["followers_mode"]

    @property
    def subscribers_mode(self) -> bool:
        return self._data["subscribers_mode"]

    @property
    def emotes_mode(self) -> bool:
        return self._data["emotes_mode"]

    @property
    def message_interval(self) -> int:
        return self._data["message_interval"]

    @property
    def following_min_duration(self) -> int:
        return self._data["following_min_duration"]

    async def connect(self) -> None:
        await self.http.ws.subscribe(self.id)

    async def send(self, content: str, /):
        print(self.id)
        data = await self.http.send_message(self.id, content)
        with open("output.html", "w") as f:
            f.write(data)
        print("sent")
