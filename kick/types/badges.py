from typing_extensions import TypedDict

from .assets import AssetSrcset


class ChatBadgePayload(TypedDict):
    type: str
    text: str
    count: int
    active: bool


class SubscriberBadgePayload(TypedDict):
    id: int
    channel_id: int
    months: int
    badge_image: AssetSrcset
