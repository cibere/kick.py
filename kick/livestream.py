from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from .assets import Asset
from .categories import Category
from .object import HTTPDataclass
from .utils import cached_property

if TYPE_CHECKING:
    from .http import HTTPClient
    from .types.videos import LivestreamPayload
    from .types.ws import PartialLivestreamPayload, LivestreamEndPayload
    from .users import User

__all__ = ("Livestream", "PartialLivestream", "LivestreamEnd")


class PartialLivestream:
    """
    A dataclass which represents a partial livestream on kick.

    Attributes
    -----------
    id: int
        The livestream's id
    channel_id: int
        The livestream's channel id
    title: str
        The livestream's title
    created_at: datetime.datetime
        When the livestream started
    streamer: `User` | None
        The livestream's streaner
    """

    def __init__(self, *, data: PartialLivestreamPayload, http: HTTPClient) -> None:
        self._data = data
        self.http = http

        self.id: int = data["id"]
        self.channel_id: int = data["channel_id"]
        self.title: str = data["session_title"]

    @cached_property
    def created_at(self) -> datetime:
        return datetime.fromisoformat(self._data["created_at"])

    @property
    def streamer(self) -> User | None:
        return self.http.client._watched_users.get(self.channel_id)


class Livestream(HTTPDataclass["LivestreamPayload"]):
    """
    A dataclass which represents a livestream on kick.

    Attributes
    -----------
    id: int
        probably the livestream's id
    slug: str
        The streamer's slug
    username: str
        The streamer's username
    channel_id: int
        probably the streamer's id or the chatroom id
    created_at: datetime.datetime
        When the livestream started
    title: str
        The livestream's title
    is_live: bool
        If the livestream is currently live
    thumbnail: `Asset` | None
        Returns the livestream's thumbnail if it has one
    duration: int
        Probably how long the livestream is/was in seconds
    language: str
        The language the livestream is in
    is_mature: bool
        If the livestream is marked as 18+
    viewer_count: int
        The amount of people currently watching
    tags: list[str]
        Tags applied to the livestream
    url: str
        The livestream's url
    embed_url: str
        The livestream's player/embed url
    categories: list[`Category`]
        The categories the livestream is in
    """

    @property
    def id(self) -> int:
        """
        probably the livestream's id
        """

        return self._data["id"]

    @property
    def slug(self) -> str:
        """
        The streamer's slug
        """

        return self._data["slug"]

    @property
    def username(self) -> str:
        """
        The streamer's username
        """

        return self._data["username"]

    @property
    def channel_id(self) -> int:
        """
        probably the streamer's id or the chatroom id
        """

        return self._data["channel_id"]

    @cached_property
    def created_at(self) -> datetime:
        """
        When the livestream started
        """

        return datetime.fromisoformat(self._data["created_at"])

    @property
    def title(self) -> str:
        """
        The livestream's title
        """

        return self._data["session_title"]

    @property
    def is_live(self) -> bool:
        """
        If the livestream is currently live
        """

        return self._data["is_live"]

    @cached_property
    def thumbnail(self) -> Asset | None:
        """
        Returns the livestream's thumbnail if it has one
        """

        return (
            None
            if self._data["thumbnail"] is None
            else Asset(url=self._data["thumbnail"]["url"], http=self.http)
        )

    @property
    def duration(self) -> int:
        """
        Probably how long the livestream is/was in seconds
        """

        return self._data["duration"]

    @property
    def language(self) -> str:
        """
        The language the livestream is in
        """

        return self._data["language"]

    @property
    def is_mature(self) -> bool:
        """
        If the livestream is marked as 18+
        """

        return self._data["is_mature"]

    @property
    def viewer_count(self) -> int:
        """
        The amount of people currently watching
        """

        return self._data["viewer_count"]

    @property
    def tags(self) -> list[str]:
        """
        Tags applied to the livestream
        """

        return self._data["tags"]

    @cached_property
    def url(self) -> str:
        """
        The livestream's url
        """

        return f"https://kick.com/{self.slug}"

    @cached_property
    def embed_url(self) -> str:
        """
        The livestream's player/embed url
        """

        return f"https://player.kick.com/{self.slug}"

    @cached_property
    def categories(self) -> list[Category]:
        """
        The categories the livestream is in
        """

        return [Category(data=c, http=self.http) for c in self._data["categories"]]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and other.id == self.id

    def __repr__(self) -> str:
        return f"<Livestream id={self.id} title={self.title} streamer={self.slug}>"

class LivestreamEnd(HTTPDataclass["LivestreamEndPayload"]):
    """
    A dataclass which represents a livestream end on kick.

    Attributes
    -----------
    id: int
        The livestream's id
    channel_id: int
        The livestream's channel id
    title: str
        The livestream's title
    streamer: `User` | None
        The livestream's streaner
    """
    @property
    def id(self) -> int:
        return self._data["id"]
    @property
    def channel_id(self):
        return self._data["channel"]["id"]

    @property
    def streamer(self) -> User | None:
        return self.http.client._watched_users.get(self.channel_id)