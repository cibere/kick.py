from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from .object import BaseDataclass
from .user import User
from .utils import MISSING

if TYPE_CHECKING:
    from .http import HTTPClient
    from .types.user import ChatterPayload

__all__ = ("Chatter",)


class Chatter(BaseDataclass["ChatterPayload"]):
    http: HTTPClient
    _following_since: datetime | None = MISSING

    @property
    def id(self) -> int:
        return self._data["id"]

    @property
    def username(self) -> str:
        return self._data["username"]

    @property
    def slug(self) -> str:
        return self._data["slug"]

    @property
    def profile_pic(self) -> str | None:
        return self._data["profile_pic"]

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

    @property
    def following_since(self) -> datetime | None:
        if self._following_since is MISSING:
            raw = self._data["following_since"]
            if raw is None:
                self._following_since = None
            else:
                self._following_since = datetime.fromisoformat(raw)
        return self._following_since

    @property
    def subscribed_for(self) -> int:
        return self._data["subscribed_for"]

    async def to_user(self) -> User:
        data = await self.http.get_user(self.username)
        user = User(data=data)
        user.http = self.http
        return user
