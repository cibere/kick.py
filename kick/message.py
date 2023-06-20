from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from .object import BaseDataclass
from .utils import cached_property

if TYPE_CHECKING:
    from .types.message import AuthorPayload, MessagePayload

__all__ = ("Author", "Message")


class Author(BaseDataclass["AuthorPayload"]):
    @property
    def id(self) -> int:
        return self._data["id"]

    @property
    def username(self) -> str:
        return self._data["slug"]

    @property
    def color(self) -> str:
        return self._data["identity"]["color"]

    @property
    def badges(self) -> list:
        """THIS IS RAW DATA"""
        return self._data["identity"]["badges"]

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Author):
            return other.id == self.id
        else:
            return False


class Message(BaseDataclass["MessagePayload"]):
    @property
    def id(self) -> str:
        return self._data["id"]

    @property
    def chatroom_id(self) -> int:
        return self._data["chatroom_id"]

    @property
    def content(self) -> str:
        return self._data["content"]

    @cached_property
    def created_at(self) -> datetime:
        return datetime.fromisoformat(self._data["created_at"])

    @cached_property
    def author(self) -> Author:
        return Author(data=self._data["sender"])

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Message) and other.id == self.id
