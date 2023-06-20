from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from .categories import Category
from .object import HTTPDataclass
from .utils import cached_property

if TYPE_CHECKING:
    from .types.videos import VideoPayload

__all__ = ("Video",)


class Video(HTTPDataclass["VideoPayload"]):
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

    @cached_property
    def updated_at(self) -> datetime:
        return datetime.fromisoformat(self._data["video"]["updated_at"])

    @property
    def session_title(self) -> str:
        return self._data["session_title"]

    @property
    def live_stream_id(self) -> int:
        return self._data["video"]["live_stream_id"]

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
            None if self._data["thumbnail"] is None else self._data["thumbnail"]["src"]
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

    @cached_property
    def categories(self) -> list[Category]:
        return [Category(data=c, http=self.http) for c in self._data["categories"]]

    def __repr__(self) -> str:
        return f"<Video id={self.id!r} streamer={self.username!r} channel_id={self.channel_id!r}>"
