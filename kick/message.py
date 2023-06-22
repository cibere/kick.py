from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from .object import HTTPDataclass
from .users import PartialUser, User
from .utils import cached_property

if TYPE_CHECKING:
    from .chatroom import Chatroom
    from .types.message import AuthorPayload, MessagePayload, ReplyMetaData

__all__ = ("Author", "Message", "PartialMessage")


class Author(HTTPDataclass["AuthorPayload"]):
    """
    Represents the author of a message on kick

    Attributes
    -----------
    id: int
        The author's id
    slug: str
        The author's slug
    color: str
        The authors... color?
    badges: list
        Unknown
    """

    @property
    def id(self) -> int:
        """
        The author's id
        """

        return self._data["id"]

    @property
    def slug(self) -> str:
        """
        The author's slug
        """

        return self._data["slug"]

    @property
    def color(self) -> str:
        """
        The authors... color?
        """

        return self._data["identity"]["color"]

    @property
    def badges(self) -> list:
        """THIS IS RAW DATA"""
        return self._data["identity"]["badges"]

    async def to_user(self) -> User:
        """
        |coro|

        Fetches a user object for the author

        Raises
        -----------
        `HTTPException`
            Fetching the user failed
        `NotFound`
            User Not Found

        Returns
        -----------
        `User`
            The user
        """

        return await self.http.client.fetch_user(self.slug)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and other.id == self.id

    def __str__(self) -> str:
        return self.slug

    def __repr__(self) -> str:
        return f"<Author id={self.id!r} slug={self.slug!r}>"


class PartialMessage(HTTPDataclass["ReplyMetaData"]):
    """
    This represents a partial message. Mainly used as the message someone is replying too.

    Attributes
    -----------
    id: str
        The message's id
    content: str
        The message's content
    author: `PartialUser`
        The message's author
    """

    @property
    def id(self) -> str:
        """
        The message's id
        """

        return self._data["original_message"]["id"]

    @property
    def content(self) -> str:
        """
        The message's content
        """

        return self._data["original_message"]["content"]

    @cached_property
    def author(self) -> PartialUser:
        """
        The message's author
        """

        return PartialUser(
            id=int(self._data["original_sender"]["id"]),
            username=self._data["original_sender"]["username"],
            http=self.http,
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and other.id == self.id

    def __repr__(self) -> str:
        return f"<Message id={self.id!r} author={self.author!r}>"


class Message(HTTPDataclass["MessagePayload"]):
    """
    Represents a message sent on kick

    Attributes
    -----------
    id: str
        the message's id
    is_reply: bool
        If the message is replying to any message
    references: `PartialMessage` | None
        If the message is replying to a message, a `PartialMessage` object is returned. Otherwise None
    chatroom_id: int
        The id of the chatroom the message was sent in
    chatroom: `Chatroom` | None
        The chatroom the message was sent in.
    content: str
        The message's content
    created_at: datetime.datetime
        When the message was sent
    author: `Author`
        The message's author
    """

    @property
    def id(self) -> str:
        """
        the message's id
        """

        return self._data["id"]

    @cached_property
    def is_reply(self) -> bool:
        """
        If the message is replying to any message
        """

        return bool(self._data.get("metadata"))

    @cached_property
    def references(self) -> PartialMessage | None:
        """
        If the message is replying to a message, a `PartialMessage` object is returned. Otherwise None
        """

        data = self._data.get("metadata")
        if not data:
            return
        return PartialMessage(data=data, http=self.http)

    @property
    def chatroom_id(self) -> int:
        """
        The id of the chatroom the message was sent in
        """

        return self._data["chatroom_id"]

    @property
    def chatroom(self) -> Chatroom | None:
        """
        The chatroom the message was sent in.
        """

        return self.http.client.get_chatroom(self.chatroom_id)

    @property
    def content(self) -> str:
        """
        The message's content
        """

        return self._data["content"]

    @cached_property
    def created_at(self) -> datetime:
        """
        When the message was sent
        """

        return datetime.fromisoformat(self._data["created_at"])

    @cached_property
    def author(self) -> Author:
        """
        The message's author
        """

        return Author(data=self._data["sender"], http=self.http)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and other.id == self.id

    def __repr__(self) -> str:
        return f"<Message id={self.id!r} chatroom={self.chatroom_id!r} author={self.author!r}>"
