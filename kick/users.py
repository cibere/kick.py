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
    from .types.user import (ClientUserPayload, InnerUser, UserPayload,
                            DestinationInfoPayload, StreamInfoPayload)

__all__ = ("DestinationInfo", "Socials", "PartialUser", "User", "ClientUser",
           "StreamInfo")

class DestinationInfo(BaseDataclass["DestinationInfoPayload"]):
    """
    Information about a user's stream destination

    Attributes
    -----------
    stream_url: str
        The URL for streaming
    stream_key: str
        The stream key
    """

    @property
    def stream_url(self) -> str:
        """The URL for streaming"""
        return self._data["rtmp_publish_path"]

    @property
    def stream_key(self) -> str:
        """The stream key"""
        return self._data["rtmp_stream_token"]


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
    """
    Base class for all user types on Kick

    Attributes
    -----------
    id: int
        The user's ID
    username: str
        The user's username
    http: HTTPClient
        The HTTP client used for requests
    """
    def __init__(self, *, id: int, username: str, http: HTTPClient) -> None:
        self.id = id
        self.username = username
        self.http = http

    async def fetch_videos(self) -> list[Video]:
        """
        |coro|

        Fetches all videos for this user

        Returns
        --------
        list[Video]
            List of videos uploaded by the user
        """
        data = await self.http.get_streamer_videos(self.username)
        return [Video(data=v, http=self.http) for v in data]

    async def fetch_gift_leaderboard(self) -> GiftLeaderboard:
        """
        |coro|

        Fetches the gift leaderboard for this user's channel

        Returns
        --------
        GiftLeaderboard
            The gift leaderboard for this channel
        """
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
    channel_id: int
        The user's channel id
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
        """The client user's ID"""
        return self._data["user_id"]

    @property
    def channel_id(self) -> int:
        return self._data["id"]

    @property
    def playback_url(self) -> str:
        return self._data["playback_url"]

    @property
    def slug(self) -> str:
        """The client user's slug (URL-friendly username)"""
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
            Asset(url=self._data["banner_image"]["url"], http=self.http)  # type: ignore
            if self._data.get("banner_image", None)
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
        """The client user's bio"""
        return self._data["user"]["bio"]

    @property
    def agreed_to_terms(self) -> bool:
        """Whether the user has agreed to Kick's terms of service"""
        return self._data["user"]["agreed_to_terms"]

    @cached_property
    def email_verified_at(self) -> datetime:
        """When the user's email was verified"""
        return datetime.fromisoformat(self._data["user"]["email_verified_at"])

    @property
    def username(self) -> str:
        """The client user's username"""
        return self._data["user"]["username"]

    @property
    def country(self) -> str:
        return self._data["user"]["country"]

    @property
    def state(self) -> str:
        return self._data["user"]["state"]

    @cached_property
    def socials(self) -> Socials:
        """The user's connected social media accounts"""
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

        chatroom = Chatroom(data=self._data["chatroom"], http=self.http, streamer=self)
        return chatroom

    @cached_property
    def recent_categories(self) -> list[Category]:
        return [
            Category(data=c, http=self.http) for c in self._data["recent_categories"]
        ]

    async def start_watch(self) -> None:
        """
        |coro|

        Watches a user to see if they go online.
        """

        await self.http.ws.watch_channel(self.channel_id)
        self.http.client._watched_users[self.channel_id] = self

    async def stop_watching(self) -> None:
        """
        |coro|

        Stops watching the user
        """

        await self.http.ws.unwatch_channel(self.channel_id)
        self.http.client._watched_users.pop(self.channel_id)

class StreamInfo(BaseDataclass["StreamInfoPayload"]):
    """
    A dataclass which represents stream information

    Attributes
    -----------
    title: str
        The stream title
    subcategory_id: int
        The ID of the game/category
    subcategory_name: Optional[str]
        The name of the game/category
    language: str
        The stream language
    is_mature: bool
        Whether the stream is marked as mature content
    """

    @property
    def title(self) -> str:
        return self._data["title"]

    @property
    def subcategory_id(self) -> int:
        return self._data["subcategoryId"]

    @property
    def subcategory_name(self) -> str | None:
        return self._data.get("subcategoryName")

    @property
    def language(self) -> str:
        return self._data["language"]

    @property
    def is_mature(self) -> bool:
        return self._data["is_mature"]

    def __repr__(self) -> str:
        return f"<StreamInfo title={self.title!r} category={self.subcategory_name!r}>"



class ClientUser(BaseUser):
    """
    Represents the connected client user

    Attributes
    -----------
    id: int
        The client user's ID
    username: str
        The client user's username
    slug: str
        The client user's slug (URL-friendly username)
    bio: str
        The client user's bio
    agreed_to_terms: bool
        Whether the user has agreed to Kick's terms of service
    email_verified_at: datetime
        When the user's email was verified
    country: str | None
        The user's country
    city: str | None
        The user's city
    state: str | None
        The user's state/province
    socials: Socials
        The user's connected social media accounts
    avatar: Asset | None
        The user's avatar image
    """
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
        """The user's country"""
        return self._data["country"]

    @property
    def city(self) -> str | None:
        """The user's city"""
        return self._data["city"]

    @property
    def state(self) -> str | None:
        """The user's state/province"""
        return self._data["state"]

    @cached_property
    def socials(self) -> Socials:
        return Socials(data=self._data)

    @cached_property
    def avatar(self) -> Asset | None:
        """The user's avatar image"""
        url = self._data["profilepic"]
        if url is None:
            return
        return Asset(url=url, http=self.http)


AnyUser = ClientUser | BaseUser | User | PartialUser
