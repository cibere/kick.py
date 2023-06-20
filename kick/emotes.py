from __future__ import annotations

from typing import TYPE_CHECKING

from .object import BaseDataclass

if TYPE_CHECKING:
    from .types.emotes import EmotePayload

__all__ = ("Emote",)


class Emote(BaseDataclass["EmotePayload"]):
    @property
    def id(self) -> int:
        return self._data["id"]

    @property
    def channel_id(self) -> int | None:
        return self._data["channel_id"]

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def subscribers_only(self) -> bool:
        return self._data["subscribers_only"]
