from __future__ import annotations

from typing import TYPE_CHECKING

from .assets import Asset
from .object import BaseDataclass, HTTPDataclass
from .utils import cached_property

if TYPE_CHECKING:
    from .types.badges import ChatBadgePayload, SubscriberBadgePayload

__all__ = ("ChatBadge", "SubscriberBadge")


class ChatBadge(BaseDataclass["ChatBadgePayload"]):
    """
    A dataclass which represents a badge from a chatroon.

    Attributes
    -----------
    type: str
        The type of badge
    text: str
        The badge's text
    count: int
        How many of that badge they have
    active: bool
        If the chatter actively has the badge
    """

    @property
    def type(self) -> str:
        """
        The type of badge
        """

        return self._data["type"]

    @property
    def text(self) -> str:
        """
        The badge's text
        """

        return self._data["text"]

    @property
    def count(self) -> int:
        """
        How many of that badge they have
        """

        return self._data["count"]

    @property
    def active(self) -> bool:
        """
        If the chatter actively has the badge
        """

        return self._data["active"]

    def __repr__(self) -> str:
        return f"<ChatBadge type={self.type!r} text={self.text!r} count={self.count!r} active={self.active!r}>"


class SubscriberBadge(HTTPDataclass["SubscriberBadgePayload"]):
    """
    A dataclass which represents a subscriber badge from a channel.

    Attributes
    -----------
    id: int
        The badge's id
    channel_id: int
        The id of the channel the chatter is subscribed too
    months: int
        How many months they have been subscribed to the chatter
    image: `Asset`
        The badge's image
    """

    @property
    def id(self) -> int:
        return self._data["id"]

    @property
    def channel_id(self) -> int:
        return self._data["channel_id"]

    @property
    def months(self) -> int:
        return self._data["months"]

    @cached_property
    def image(self) -> Asset:
        return Asset._from_asset_src(data=self._data["badge_image"], http=self.http)

    def __repr__(self) -> str:
        return f"<SubscriberBadge id={self.id!r} channel_id={self.channel_id!r} months={self.months!r} image={self.image!r}>"
