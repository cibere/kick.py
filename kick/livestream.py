from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from .categories import Category
from .object import BaseDataclass
from .utils import cached_property

if TYPE_CHECKING:
    from .types.videos import LivestreamPayload

__all__ = ("Livestream",)


class Livestream(BaseDataclass["LivestreamPayload"]):
    @property
    def id(self) -> int:
        return self._data["id"]

    @property
    def username(self) -> str:
        return self._data["slug"]

    @property
    def channel_id(self) -> int:
        return self._data["channel_id"]

    @cached_property
    def created_at(self) -> datetime:
        return datetime.fromisoformat(self._data["created_at"])

    @property
    def session_title(self) -> str:
        return self._data["session_title"]

    @property
    def is_live(self) -> bool:
        return self._data["is_live"]

    @property
    def risk_level_id(self) -> Any:
        """THIS IS RAW DATA, UNKNOWN ON WHAT IT RETURNS"""
        return self._data["risk_level_id"]

    @property
    def source(self) -> Any:
        """THIS IS RAW DATA, UNKNOWN ON WHAT IT RETURNS"""
        return self._data["source"]

    @property
    def twitch_channel(self) -> Any:
        """THIS IS RAW DATA, UNKNOWN ON WHAT IT RETURNS"""
        return self._data["twitch_channel"]

    @property
    def thumbnail(self) -> str | None:
        return (
            None if self._data["thumbnail"] is None else self._data["thumbnail"]["url"]
        )

    @property
    def duration(self) -> int:
        return self._data["duration"]

    @property
    def language(self) -> str:
        return self._data["language"]

    @property
    def is_mature(self) -> bool:
        return self._data["is_mature"]

    @property
    def viewer_count(self) -> int:
        return self._data["viewer_count"]

    @property
    def tags(self) -> list[Any]:
        """THIS IS RAW DATA, UNKNOWN ON WHAT IT RETURNS BESIDES `list`"""
        return self._data["tags"]

    @cached_property
    def categories(self) -> list[Category]:
        return [Category(data=c) for c in self._data["categories"]]
