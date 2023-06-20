from typing_extensions import TypedDict

from .assets import AssetSrcset, AssetUrl
from .categories import Category


class BaseVideoPayload(TypedDict):
    id: int
    slug: str
    channel_id: int
    created_at: str
    session_title: str
    is_live: bool
    risk_level_id: None  # NEED TO FIGURE THIS OUT
    source: None  # NEED TO FIGURE THIS OUT
    twitch_channel: None  # NEED TO FIGURE THIS OUT
    duration: int
    language: str
    is_mature: bool
    viewer_count: int
    categories: list[Category]


class LivestreamPayload(BaseVideoPayload):
    tags: list  # NEED TO FIGURE THIS OUT
    thumbnail: None | AssetUrl


class InnerVideoPayload(TypedDict):
    id: int
    live_stream_id: int
    slug: str | None  # Assumed str
    thumb: None  # NEED TO FIGURE THIS OUT
    s3: None  # NEED TO FIGURE THIS OUT
    trading_platform_id: None  # NEED TO FIGURE THIS OUT
    created_at: str
    updated_at: str
    views: int
    deleted_at: None  # NEED TO FIGURE THIS OUT


class VideoPayload(BaseVideoPayload):
    video: InnerVideoPayload
    thumbnail: AssetSrcset
