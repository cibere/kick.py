from __future__ import annotations

from typing import TYPE_CHECKING

from .assets import Asset
from .object import HTTPDataclass
from .utils import cached_property

if TYPE_CHECKING:
    from .types.emotes import EmotePayload

__all__ = ("Emote",)


class Emote(HTTPDataclass["EmotePayload"]):
    @property
    def id(self) -> int:
        return self._data["id"]

    @cached_property
    def is_global(self) -> bool:
        return bool(self._data["channel_id"])

    @property
    def channel_id(self) -> int | None:
        return self._data["channel_id"]

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def subscribers_only(self) -> bool:
        return self._data["subscribers_only"]

    @cached_property
    def source(self) -> Asset:
        return Asset._from_emote(self.id, http=self.http)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and other.id == self.id

    def __str__(self) -> str:
        return self.name
