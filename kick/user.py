from __future__ import annotations

from typing import TYPE_CHECKING

from .chatroom import Chatroom
from .object import BaseDataclass

if TYPE_CHECKING:
    from .http import HTTPClient
    from .types.user import InnerUser, UserPayload

__all__ = ("User", "Socials")


class Socials(BaseDataclass[InnerUser]):
    @property
    def instagram(self) -> str:
        return self.__data["instagram"]

    @property
    def youtube(self) -> str:
        return self.__data["youtube"]

    @property
    def twitter(self) -> str:
        return self.__data["twitter"]

    @property
    def discord(self) -> str:
        return self.__data["discord"]

    @property
    def tiktok(self) -> str:
        return self.__data["tiktok"]

    @property
    def facebook(self) -> str:
        return self.__data["facebook"]


class User(BaseDataclass[UserPayload]):
    _socials: Socials | None = None
    _chatroom: Chatroom | None = None
    http: HTTPClient

    @property
    def id(self) -> int:
        return self.__data["user_id"]

    @property
    def slug(self) -> str:
        return self.__data["slug"]

    @property
    def vod_enabled(self) -> bool:
        return self.__data["vod_enabled"]

    @property
    def is_banned(self) -> bool:
        return self.__data["is_banned"]

    @property
    def subscription_enabled(self) -> bool:
        return self.__data["subscription_enabled"]

    @property
    def follower_count(self) -> int:
        return self.__data["followers_count"]

    @property
    def subscriber_badges(self) -> list:
        """THIS IS RAW DATA"""
        return self.__data["subscriber_badges"]

    @property
    def follower_badges(self) -> list:
        """THIS IS RAW DATA"""
        return self.__data["follower_badges"]

    @property
    def online_banner_url(self) -> str | None:
        return (
            self.__data["banner_image"]["url"] if self.__data["banner_image"] else None
        )

    @property
    def offline_banner_url(self) -> str | None:
        return (
            self.__data["offline_banner_image"]["src"]
            if self.__data["offline_banner_image"]
            else None
        )

    @property
    def is_muted(self) -> bool:
        return self.__data["muted"]

    @property
    def is_verified(self) -> bool:
        return self.__data["verified"]

    @property
    def avatar_url(self) -> str:
        return self.__data["user"]["profile_pic"]

    @property
    def can_host(self) -> bool:
        return self.__data["can_host"]

    @property
    def country(self) -> str:
        return self.__data["user"]["country"]

    @property
    def state(self) -> str:
        return self.__data["user"]["state"]

    @property
    def socials(self) -> Socials:
        if self._socials is None:
            self._socials = Socials(data=self.__data["user"])
        return self._socials

    @property
    def chatroom(self) -> Chatroom:
        if self._chatroom is None:
            self._chatroom = Chatroom(data=self.__data["chatroom"])
            self._chatroom.http = self.http
        return self._chatroom

    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return other.id == self.id
        else:
            return False
