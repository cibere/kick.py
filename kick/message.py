from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from .object import BaseDataclass
from .utils import cached_property

if TYPE_CHECKING:
    from .types.message import (
        AuthorPayload,
        MessagePayload,
        ReplyMetaData,
        ReplyOriginalSender,
    )

__all__ = ("Author", "Message", "PartialAuthor", "PartialMessage")


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
        return isinstance(other, self.__class__) and other.id == self.id


class PartialAuthor(BaseDataclass["ReplyOriginalSender"]):
    @cached_property
    def id(self) -> int:
        return int(self._data["id"])

    @property
    def username(self) -> str:
        return self._data["username"]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and other.id == self.id


class PartialMessage(BaseDataclass["ReplyMetaData"]):
    @property
    def id(self) -> str:
        return self._data["original_message"]["id"]

    @property
    def content(self) -> str:
        return self._data["original_message"]["content"]

    @cached_property
    def author(self) -> PartialAuthor:
        return PartialAuthor(data=self._data["original_sender"])

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and other.id == self.id


class Message(BaseDataclass["MessagePayload"]):
    @property
    def id(self) -> str:
        return self._data["id"]

    @cached_property
    def is_reply(self) -> bool:
        return bool(self._data.get("metadata"))

    @cached_property
    def references(self) -> PartialMessage | None:
        data = self._data.get("metadata")
        if not data:
            return
        return PartialMessage(data=data)

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
        return isinstance(other, self.__class__) and other.id == self.id
