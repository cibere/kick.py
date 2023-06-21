from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from .assets import Asset
from .badges import ChatBadge
from .object import HTTPDataclass
from .user import User
from .utils import cached_property

if TYPE_CHECKING:
    from .chatroom import Chatroom
    from .types.user import ChatterPayload

__all__ = ("Chatter",)


class Chatter(HTTPDataclass["ChatterPayload"]):
    chatroom: Chatroom

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
    def is_mod(self) -> bool:
        return self._data["is_moderator"]

    @cached_property
    def badges(self) -> list[ChatBadge]:
        return [ChatBadge(data=c) for c in self._data["badges"]]

    @cached_property
    def following_since(self) -> datetime | None:
        raw = self._data["following_since"]
        if raw is None:
            return
        else:
            return datetime.fromisoformat(raw)

    @property
    def subscribed_for(self) -> int:
        """
        The amount of months the user has been subscribed for
        """

        return self._data["subscribed_for"]

    async def to_user(self) -> User:
        data = await self.http.get_user(self.username)
        user = User(data=data, http=self.http)
        return user

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and other.id == self.id

    def __str__(self) -> str:
        return self.username

    def __repr__(self) -> str:
        return f"<Chatter id={self.id!r} username={self.username!r} profile_pic={self.profile_pic!r} is_staff={self.is_staff!r} is_channel_owner={self.is_channel_owner!r} is_mod={self.is_mod!r}>"
