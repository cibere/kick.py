from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from .object import BaseDataclass

if TYPE_CHECKING:
    from .types.message import AuthorPayload, MessagePayload

__all__ = ("Author", "Message")


class Author(BaseDataclass[AuthorPayload]):
    @property
    def id(self) -> int:
        return self.__data["id"]

    @property
    def username(self) -> str:
        return self.__data["slug"]

    @property
    def color(self) -> str:
        return self.__data["identity"]["color"]

    @property
    def badges(self) -> list:
        """THIS IS RAW DATA"""
        return self.__data["identity"]["badges"]

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Author):
            return other.id == self.id
        else:
            return False


class Message(BaseDataclass[MessagePayload]):
    _author: Author | None = None
    _timestamp: datetime | None

    @property
    def id(self) -> str:
        return self.__data["id"]

    @property
    def chatroom_id(self) -> int:
        return self.__data["chatroom_id"]

    @property
    def content(self) -> str:
        return self.__data["content"]

    @property
    def created_at(self) -> datetime:
        if self._timestamp is None:
            self._timestamp = datetime.fromisoformat(self.__data["created_at"])
        return self._timestamp

    @property
    def author(self) -> Author:
        if self._author is None:
            self._author = Author(data=self.__data["sender"])
        return self._author

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Message):
            return other.id == self.id
        else:
            return False
