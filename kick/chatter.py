from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from .assets import Asset
from .badges import ChatBadge
from .object import HTTPDataclass
from .users import User
from .utils import cached_property

if TYPE_CHECKING:
    from .chatroom import Chatroom
    from .types.user import ChatterPayload

__all__ = ("Chatter",)


class Chatter(HTTPDataclass["ChatterPayload"]):
    """
    A dataclass which respresents a chatter on kick

    Attributes
    -----------
    chatroom: Chatroom
        The chatroom the chatter is in
    id: int
        The chatter's id
    username: str
        The chatter's username
    slug: str
        The chatter' slug
    avatar: `Asset` | None
        The chatter's avatar, if any
    is_staff: bool
        If the chatter is a staff member in the chatroom
    is_owner: bool
        If the chatter is the chatroom owner
    is_mod: bool
        If the chatter is a mod in the chatroom
    badges: list[`ChatBadge`]
        The chat badges the chatter has
    following_since: datetime.datetime | None
        when the chatter started following the streamer
    """

    chatroom: Chatroom

    @property
    def id(self) -> int:
        """
        The chatter's id
        """

        return self._data["id"]

    @property
    def username(self) -> str:
        """
        The chatter's username
        """

        return self._data["username"]

    @property
    def slug(self) -> str:
        """
        The chatter' slug
        """

        return self._data["slug"]

    @cached_property
    def avatar(self) -> Asset | None:
        """
        The chatter's avatar, if any
        """

        return (
            None
            if self._data["profile_pic"] is None
            else Asset(url=self._data["profile_pic"], http=self.http)
        )

    @property
    def is_staff(self) -> bool:
        """
        If the chatter is a staff member in the chatroom
        """

        return self._data["is_staff"]

    @property
    def is_owner(self) -> bool:
        """
        If the chatter is the chatroom owner
        """

        return self._data["is_channel_owner"]

    @property
    def is_mod(self) -> bool:
        """
        If the chatter is a mod in the chatroom
        """

        return self._data["is_moderator"]

    @cached_property
    def badges(self) -> list[ChatBadge]:
        """
        The chat badges the chatter has
        """

        return [ChatBadge(data=c) for c in self._data["badges"]]

    @cached_property
    def following_since(self) -> datetime | None:
        """
        when the chatter started following the streamer
        """

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
        """
        |coro|

        Fetches a user object for the chatter

        Raises
        -----------
        `HTTPException`
            Fetching the user failed
        `NotFound`
            User not found

        Returns
        -----------
        `User`
            The user
        """
        data = await self.http.get_user(self.username)
        user = User(data=data, http=self.http)
        return user

    async def ban(self, reason: str) -> None:
        """
        |coro|

        Permanently bans a user from a chatroom.

        Parameters
        -----------
        reason: str
            The reason for the ban

        Raises
        -----------
        `HTTPException`
            Banning the user failed
        `Forbidden`
            You are unauthorized from banning the user
        `NotFound`
            Streamer or user not found
        """

        await self.http.ban_chatter(self.chatroom.streamer.slug, self.slug, reason)

    async def timeout(self, duration: int, *, reason: str) -> None:
        """
        |coro|

        Times out a user for a given amount of time.

        Parameters
        -----------
        duration: int
            The amount of seconds for the timeout to be
        reason: str
            The reason for the timeout

        Raises
        -----------
        `HTTPException`
            timing out the user failed
        `Forbidden`
            You are unauthorized from timing out the user
        `NotFound`
            Streamer or user not found
        """

        await self.http.timeout_chatter(
            self.chatroom.streamer.slug, self.slug, reason, duration
        )

    async def unban(self) -> None:
        """
        |coro|

        Unbans the chatter from the chatroom

        Raises
        -----------
        `HTTPException`
            Unbanning the user failed
        `Forbidden`
            You are unauthorized from unbanning the user
        `NotFound`
            Streamer or user not found
        """

        await self.http.unban_user(self.chatroom.streamer.slug, self.slug)

    async def untimeout(self) -> None:
        """
        |coro|

        untimeout's the chatter

        Raises
        -----------
        `HTTPException`
            untimeouting the user failed
        `Forbidden`
            You are unauthorized from untimeouting the user
        `NotFound`
            Streamer or user not found
        """

        await self.http.unban_user(self.chatroom.streamer.slug, self.slug)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and other.id == self.id

    def __str__(self) -> str:
        return self.username

    def __repr__(self) -> str:
        return f"<Chatter id={self.id!r} username={self.username!r} avatar={self.avatar!r} is_staff={self.is_staff!r} is_owner={self.is_owner!r} is_mod={self.is_mod!r}>"
