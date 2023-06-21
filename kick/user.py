from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from kick.categories import Category

from .assets import Asset
from .badges import SubscriberBadge
from .leaderboard import GiftLeaderboard
from .livestream import Livestream
from .object import BaseDataclass, HTTPDataclass
from .utils import cached_property
from .videos import Video

if TYPE_CHECKING:
    from .chatroom import Chatroom
    from .types.user import (
        ClientUserPayload,
        InnerUser,
        PartialUserPayload,
        UserPayload,
    )

__all__ = ("User", "Socials", "PartialUser", "ClientUser")


class Socials(BaseDataclass["InnerUser | ClientUserPayload"]):
    @property
    def instagram(self) -> str:
        return self._data["instagram"] or ""

    @property
    def youtube(self) -> str:
        return self._data["youtube"] or ""

    @property
    def twitter(self) -> str:
        return self._data["twitter"] or ""

    @property
    def discord(self) -> str:
        return self._data["discord"] or ""

    @property
    def tiktok(self) -> str:
        return self._data["tiktok"] or ""

    @property
    def facebook(self) -> str:
        return self._data["facebook"] or ""


class PartialUser(HTTPDataclass["PartialUserPayload"]):
    @cached_property
    def id(self) -> int:
        return int(self._data["id"])

    @property
    def username(self) -> str:
        return self._data["username"]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and other.id == self.id

    def __str__(self) -> str:
        return self.username

    def __repr__(self) -> str:
        return f"<PartialUser id={self.id!r} username={self.username!r}>"

    async def fetch(self) -> User:
        data = await self.http.get_user(self.username)
        return User(data=data, http=self.http)


class User(HTTPDataclass["UserPayload"]):
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

    async def fetch_videos(self) -> list[Video]:
        data = await self.http.get_streamer_videos(self.slug)
        return [Video(data=v, http=self.http) for v in data]

    async def fetch_gift_leaderboard(self) -> GiftLeaderboard:
        data = await self.http.get_channel_gift_leaderboard(self.slug)
        leaderboard = GiftLeaderboard(data=data)
        leaderboard.streamer = self
        return leaderboard

    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return other.id == self.id
        else:
            return False

    def __str__(self) -> str:
        return self.username

    def __repr__(self) -> str:
        return f"<User id={self.id!r} name={self.username!r}>"


class ClientUser(HTTPDataclass["ClientUserPayload"]):
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

    async def fetch_videos(self) -> list[Video]:
        data = await self.http.get_streamer_videos(self.slug)
        return [Video(data=v, http=self.http) for v in data]

    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return other.id == self.id
        else:
            return False

    def __str__(self) -> str:
        return self.username

    def __repr__(self) -> str:
        return f"<ClientUser id={self.id!r} name={self.username!r}>"
