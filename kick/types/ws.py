from typing_extensions import TypedDict

from .assets import AssetSrcset, AssetUrl
from .categories import Category


class PartialLivestreamPayload(TypedDict):
    id: int
    channel_id: int
    session_title: str
    source: None  # Unknown
    created_at: str


class FollowersUpdatePayload(TypedDict):
    followersCount: str
    channel_id: int
    username: None | str
    created_at: int
    followed: bool


class LivestreamEndPayload(TypedDict):
    id: int
    channel_id: int
    is_banned: bool