from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from .assets import Asset
from .object import HTTPDataclass
from .user import User
from .utils import cached_property

if TYPE_CHECKING:
    from .types.user import ChatterPayload

__all__ = ("Chatter",)


class Chatter(HTTPDataclass["ChatterPayload"]):
    @property
    def id(self) -> int:
        return self._data["id"]

    @property
    def username(self) -> str:
        return self._data["username"]

    @property
    def slug(self) -> str:
        return self._data["slug"]

    @cached_property
    def profile_pic(self) -> Asset | None:
        return (
            None
            if self._data["profile_pic"] is None
            else Asset(url=self._data["profile_pic"], http=self.http)
        )

    @property
    def is_staff(self) -> bool:
        return self._data["is_staff"]

    @property
    def is_channel_owner(self) -> bool:
        return self._data["is_channel_owner"]

    @property
    def is_moderator(self) -> bool:
        return self._data["is_moderator"]

    @property
    def badges(self) -> list:
        """THIS IS RAW DATA"""
        return self._data["badges"]

    @cached_property
    def following_since(self) -> datetime | None:
        raw = self._data["following_since"]
        if raw is None:
            return
        else:
            return datetime.fromisoformat(raw)

    @property
    def subscribed_for(self) -> int:
        return self._data["subscribed_for"]

    async def to_user(self) -> User:
        data = await self.http.get_user(self.username)
        user = User(data=data, http=self.http)
        return user

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and other.id == self.id

    def __str__(self) -> str:
        return self.username
