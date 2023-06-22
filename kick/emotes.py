from __future__ import annotations

from typing import TYPE_CHECKING

from .assets import Asset
from .object import HTTPDataclass
from .utils import cached_property

if TYPE_CHECKING:
    from .types.emotes import EmotePayload

__all__ = ("Emote",)


class Emote(HTTPDataclass["EmotePayload"]):
    """
    A dataclass which represents an emote on kick.

    Attributes
    -----------
    id: int
        The emote's id
    is_global: bool
        If the emote is a global emote, or from a channel
    channel_id: int | None
        returns the channel_id the emote is from, or None if global
    name: str
        The emote's name
    subscribers_only: bool
        If you have to be a subscriber of the channel to use it. False for global emotes
    source: `Asset`
        An asset which contains the emote's source.
    """

    @property
    def id(self) -> int:
        """
        The emote's id
        """

        return self._data["id"]

    @cached_property
    def is_global(self) -> bool:
        """
        If the emote is a global emote, or from a channel
        """

        return bool(self._data["channel_id"])

    @property
    def channel_id(self) -> int | None:
        """
        returns the channel_id the emote is from, or None if global
        """

        return self._data["channel_id"]

    @property
    def name(self) -> str:
        """
        The emote's name
        """

        return self._data["name"]

    @property
    def subscribers_only(self) -> bool:
        """
        If you have to be a subscriber of the channel to use it. False for global emotes
        """

        return self._data["subscribers_only"]

    @cached_property
    def source(self) -> Asset:
        """
        An asset which contains the emote's source.
        """

        return Asset._from_emote(self.id, http=self.http)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and other.id == self.id

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return (
            f"<Emote id={self.id!r} channel_id={self.channel_id!r} name={self.name!r}>"
        )
