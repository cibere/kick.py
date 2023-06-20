from __future__ import annotations

import asyncio
from logging import getLogger
from typing import TYPE_CHECKING, Any, Callable, Coroutine, TypeVar

from .http import HTTPClient
from .message import Message
from .user import User
from .utils import MISSING

if TYPE_CHECKING:
    from typing_extensions import Self

EventT = TypeVar("EventT", bound=Callable[..., Coroutine[Any, Any, None]])
LOGGER = getLogger(__name__)

__all__ = ("Credentials", "Client")


class Credentials:
    def __init__(
        self,
        *,
        username: str = MISSING,
        email: str = MISSING,
        password: str,
        one_time_password: str | None = None,
    ) -> None:
        if username is MISSING and email is MISSING:
            raise ValueError("Provide either a `username` or `email` arg")
        elif username is not MISSING and email is not MISSING:
            raise ValueError("Provide `username` or `email`, not both.")

        self.email: str = username or email
        self.password: str = password
        self.one_time_password: str | None = one_time_password


class Client:
    def __init__(self, **options: Any) -> None:
        self._options = options
        self.http = HTTPClient(self)

    async def fetch_user(self, streamer: str) -> User:
        data = await self.http.get_user(streamer)
        user = User(data=data, http=self.http)
        return user

    def dispatch(self, event_name: str, *args, **kwargs) -> None:
        event_name = f"on_{event_name}"

        event = getattr(self, event_name, None)
        if event is not None:
            asyncio.create_task(
                event(*args, **kwargs), name=f"event-dispatch: {event_name}"
            )

    def event(self, coro: EventT) -> EventT:
        setattr(self, coro.__name__, coro)
        return coro

    async def login(self, credentials: Credentials) -> None:
        await self.http.login(credentials)

    async def start(self, credentials: Credentials | None = None) -> None:
        LOGGER.warning(
            "Kick.py is in early alpha, and might not work as intended. Use at your own risk."
        )
        if credentials is not None:
            await self.http.login(credentials)
        await self.http.start()

    async def close(self) -> None:
        await self.http.close()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    async def on_ready(self) -> None:
        ...

    async def on_message(self, msg: Message) -> None:
        ...
