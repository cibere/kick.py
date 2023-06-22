from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from kick.assets import Asset

from .categories import Category
from .object import HTTPDataclass
from .utils import cached_property

if TYPE_CHECKING:
    from .types.videos import VideoPayload

__all__ = ("Video",)


class Video(HTTPDataclass["VideoPayload"]):
    """
    This dataclass represents a video on kick

    Attributes
    -----------
    id: int
        The video's id
    slug: str
        the video's slug
    channel_id: int
        Probably the id of the channel the video is from
    created_at: datetime.datetime
        When the video was created
    updated_at: datetime.datetime
        When the video was last updated
    title: str
        The video's title
    live_stream_id: int
        The id of the live stream the video is from
    thumbnail: `Asset` | None
        The video's thumbnail
    duration: int
        How long the video is in seconds
    language: str
        The language the video is in
    is_mature: bool
        If the video is marked as 18+
    viewer_count: int
        How many people have seen the video
    categories: list[`Category`]
        The categories the video is in
    """

    @property
    def id(self) -> int:
        """
        The video's id
        """

        return self._data["id"]

    @property
    def slug(self) -> str:
        """
        the video's slug
        """

        return self._data["slug"]

    @property
    def channel_id(self) -> int:
        """
        Probably the id of the channel the video is from
        """

        return self._data["channel_id"]

    @cached_property
    def created_at(self) -> datetime:
        """
        When the video was created
        """

        return datetime.fromisoformat(self._data["created_at"])

    @cached_property
    def updated_at(self) -> datetime:
        """
        When the video was last updated
        """

        return datetime.fromisoformat(self._data["video"]["updated_at"])

    @property
    def title(self) -> str:
        """
        The video's title
        """

        return self._data["session_title"]

    @property
    def live_stream_id(self) -> int:
        """
        The id of the live stream the video is from
        """

        return self._data["video"]["live_stream_id"]

    @property
    def thumbnail(self) -> Asset | None:
        """
        The video's thumbnail
        """

        return (
            None
            if self._data["thumbnail"] is None
            else Asset._from_asset_src(data=self._data["thumbnail"], http=self.http)
        )

    @property
    def duration(self) -> int:
        """
        How long the video is in seconds
        """

        return self._data["duration"]

    @property
    def language(self) -> str:
        """
        The language the video is in
        """

        return self._data["language"]

    @property
    def is_mature(self) -> bool:
        """
        If the video is marked as 18+
        """

        return self._data["is_mature"]

    @property
    def viewer_count(self) -> int:
        """
        How many people have seen the video
        """

        return self._data["viewer_count"]

    @cached_property
    def categories(self) -> list[Category]:
        """
        The categories the video is in
        """

        return [Category(data=c, http=self.http) for c in self._data["categories"]]

    def __repr__(self) -> str:
        return (
            f"<Video id={self.id!r} slug={self.slug!r} channel_id={self.channel_id!r}>"
        )
