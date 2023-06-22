from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from kick.categories import Category

from .assets import Asset
from .badges import SubscriberBadge
from .leaderboard import GiftLeaderboard
from .livestream import Livestream
from .object import BaseDataclass
from .utils import cached_property
from .videos import Video

if TYPE_CHECKING:
    from .chatroom import Chatroom
    from .http import HTTPClient
    from .types.user import ClientUserPayload, InnerUser, UserPayload

__all__ = ("User", "Socials", "PartialUser", "ClientUser")


class Socials(BaseDataclass["InnerUser | ClientUserPayload"]):
    """
    The socials a user on kick has added to their profile

    Attributes
    -----------
    instagram: str
        Their instagram
    youtube: str
        Their youtube
    twitter: str
        Their twitter
    discord: str
        Their discord
    tiktok: str
        Their tiktok
    facebook: str
        Their facebook
    """

    @property
    def instagram(self) -> str:
        """
        Their instagram
        """

        return self._data["instagram"] or ""

    @property
    def youtube(self) -> str:
        """
        Their youtube
        """

        return self._data["youtube"] or ""

    @property
    def twitter(self) -> str:
        """
        Their twitter
        """

        return self._data["twitter"] or ""

    @property
    def discord(self) -> str:
        """
        Their discord
        """

        return self._data["discord"] or ""

    @property
    def tiktok(self) -> str:
        """
        Their tiktok
        """

        return self._data["tiktok"] or ""

    @property
    def facebook(self) -> str:
        """
        Their facebook
        """

        return self._data["facebook"] or ""


class BaseUser:
    def __init__(self, *, id: int, username: str, http: HTTPClient) -> None:
        self.id = id
        self.username = username
        self.http = http

    async def fetch_videos(self) -> list[Video]:
        data = await self.http.get_streamer_videos(self.username)
        return [Video(data=v, http=self.http) for v in data]

    async def fetch_gift_leaderboard(self) -> GiftLeaderboard:
        data = await self.http.get_channel_gift_leaderboard(self.username)
        leaderboard = GiftLeaderboard(data=data)
        leaderboard.streamer = self
        return leaderboard

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and other.id == self.id

    def __str__(self) -> str:
        return self.username

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id!r} username={self.username!r}>"


class PartialUser(BaseUser):
    """
    This dataclass represents a partial user on kick

    Attributes
    -----------
    id: int
        The user's id
    username: str
        The user's name
    """

    async def fetch(self) -> User:
        """
        |coro|

        Fetches a full user object

        Raises
        -----------
        `HTTPException`
            Fetching the user failed
        `NotFound`
            User not found

        Returns
        -----------
        `User`
            The full user object
        """

        data = await self.http.get_user(self.username)
        return User(data=data, http=self.http)


class User:
    """
    A dataclass which represents a User on kick

    Attributes
    -----------
    id: int
        The user's id
    username: str
        The user's name
    state: str
        The state the user has said they live in
    socials: `Socials`
        The socials the user has said they have
    country: str
        The country the user has said they live in
    playback_url: str
        The user's playback url
    slug: str
        The user's slug
    vod_enabled: bool
        If the user has vods enabled
    is_banned: bool
        If the user is banned
    subscription_enabled: bool
        If the user has subscriptions enabled
    follower_count: int
        The amount of followers the user has
    subscriber_badges: list[`SubscriberBadge`]
        A list of subscriber badges the user has
    online_banner: `Asset` | None
        the banner that gets displayed when the user is live
    offline_banner: `Asset` | None
        the banner that gets displayed when the user is offline
    is_muted: bool
        If the user is muted
    is_verified: bool
        If the user is verified
    avatar: `Asset`
        The user's avatar
    can_host: bool
        If the user can host
    bio: str
        The user's bio
    agreed_to_terms: bool
        if the user has agreed to kick's TOS
    email_verified_at: datetime.datetime
        When the user verified their user
    livestream: `Livestream` | None
        The user's livestream
    chatroom: `Chatroom`
        The user's chatroom
    recent_categories: list[`Category`]
        The categories the user has recently gone live in
    """

    def __init__(self, *, data: UserPayload, http: HTTPClient) -> None:
        self._data = data
        self.http = http

    @property
    def id(self) -> int:
        return self._data["user_id"]

    @property
    def playback_url(self) -> str:
        return self._data["playback_url"]

    @property
    def slug(self) -> str:
        return self._data["slug"]

    @property
    def vod_enabled(self) -> bool:
        return self._data["vod_enabled"]

    @property
    def is_banned(self) -> bool:
        return self._data["is_banned"]

    @property
    def subscription_enabled(self) -> bool:
        return self._data["subscription_enabled"]

    @property
    def follower_count(self) -> int:
        return self._data["followers_count"]

    @property
    def subscriber_badges(self) -> list[SubscriberBadge]:
        return [
            SubscriberBadge(data=c, http=self.http)
            for c in self._data["subscriber_badges"]
        ]

    @property
    def follower_badges(self) -> list:
        """THIS IS RAW DATA"""
        return self._data["follower_badges"]

    @cached_property
    def online_banner(self) -> Asset | None:
        return (
            Asset(url=self._data["banner_image"]["url"], http=self.http)
            if self._data["banner_image"]
            else None
        )

    @cached_property
    def offline_banner(self) -> Asset | None:
        return (
            Asset._from_asset_src(
                data=self._data["offline_banner_image"], http=self.http
            )
            if self._data["offline_banner_image"]
            else None
        )

    @property
    def is_muted(self) -> bool:
        return self._data["muted"]

    @property
    def is_verified(self) -> bool:
        return self._data["verified"]

    @cached_property
    def avatar(self) -> Asset:
        return Asset(url=self._data["user"]["profile_pic"], http=self.http)

    @property
    def can_host(self) -> bool:
        return self._data["can_host"]

    @property
    def bio(self) -> str:
        return self._data["user"]["bio"]

    @property
    def agreed_to_terms(self) -> bool:
        return self._data["user"]["agreed_to_terms"]

    @cached_property
    def email_verified_at(self) -> datetime:
        return datetime.fromisoformat(self._data["user"]["email_verified_at"])

    @property
    def username(self) -> str:
        return self._data["user"]["username"]

    @property
    def country(self) -> str:
        return self._data["user"]["country"]

    @property
    def state(self) -> str:
        return self._data["user"]["state"]

    @cached_property
    def socials(self) -> Socials:
        return Socials(data=self._data["user"])

    @cached_property
    def livestream(self) -> Livestream | None:
        livestream = self._data["livestream"]
        if not livestream:
            return
        return Livestream(data=livestream, http=self.http)

    @cached_property
    def chatroom(self) -> Chatroom:
        from .chatroom import Chatroom

        chatroom = Chatroom(data=self._data["chatroom"], http=self.http)
        chatroom.streamer = self
        return chatroom

    @cached_property
    def recent_categories(self) -> list[Category]:
        return [
            Category(data=c, http=self.http) for c in self._data["recent_categories"]
        ]


class ClientUser(BaseUser):
    def __init__(self, *, data: ClientUserPayload, http: HTTPClient) -> None:
        self._data = data
        self.http = http

    @property
    def id(self) -> int:
        return self._data["id"]

    @property
    def username(self) -> str:
        return self._data["username"]

    @property
    def slug(self) -> str:
        return self._data["username"].lower().replace("_", "-")

    @property
    def bio(self) -> str:
        return self._data["bio"] or ""

    @property
    def agreed_to_terms(self) -> bool:
        return self._data["agreed_to_terms"]

    @cached_property
    def email_verified_at(self) -> datetime:
        return datetime.fromisoformat(self._data["email_verified_at"])

    @property
    def country(self) -> str | None:
        return self._data["country"]

    @property
    def city(self) -> str | None:
        return self._data["city"]

    @property
    def state(self) -> str | None:
        return self._data["state"]

    @cached_property
    def socials(self) -> Socials:
        return Socials(data=self._data)

    @cached_property
    def avatar(self) -> Asset | None:
        url = self._data["profilepic"]
        if url is None:
            return
        return Asset(url=url, http=self.http)


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


AnyUser = ClientUser | BaseUser | User | PartialUser
