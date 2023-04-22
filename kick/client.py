from __future__ import annotations

import asyncio

from .http import HTTPClient
from .message import Message
from .user import User


class Client:
    def __init__(self, token: str) -> None:
        self.http = HTTPClient(token)

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
        ...
