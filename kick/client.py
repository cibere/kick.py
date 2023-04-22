from __future__ import annotations

import asyncio
from types import TracebackType
from typing import TYPE_CHECKING, Type

from .http import HTTPClient
from .message import Message
from .user import User

if TYPE_CHECKING:
    from typing_extensions import Self


class Client:
    def __init__(self, token: str) -> None:
        self.http = HTTPClient(token, self)

    async def get_user(self, streamer: str) -> User:
        data = await self.http.get_user(streamer)
        user = User(data=data)
        user.http = self.http
        return user

    async def dispatch(self, event_name: str, *args, **kwargs) -> None:
        event_name = f"on_{event_name}"

        event = getattr(self, event_name, None)
        if event is not None:
            asyncio.create_task(
                event(*args, **kwargs), name=f"event-dispatch: {event_name}"
            )

    async def on_message(self, msg: Message) -> None:
        print(f"Received message from {msg.author.username}")

    async def start(self) -> None:
        ws = await self.http.create_ws()
        await ws.start()

    async def close(self) -> None:
        await self.http.close()

    async def __aenter__(self) -> Self:
        await self.start()
        return self

    async def __aexit__(
        self, exc_type: Type[Exception], exc: Exception, tb: TracebackType
    ) -> None:
        await self.close()
