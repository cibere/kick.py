from typing import Any, Generic, TypeVar

from typing_extensions import TypedDict

from .user import InnerUser

EmojiNameT = TypeVar("EmojiNameT", bound=str)


class EmotePayload(TypedDict):
    id: int
    channel_id: None  # NEED TO FIGURE THIS OUT
    name: str
    subscribers_only: bool


class EmojiUserPayload(TypedDict):
    id: int
    user_id: int
    slug: str
    is_banned: bool
    playback_url: str
    name_updated_at: None  # NEED TO FIGURE THIS OUT
    vod_enabled: bool
    subscription_enabled: bool
    cf_rate_limiter: str
    emotes: list[EmotePayload]
    can_host: bool
    user: InnerUser


class EmotesDataPayload(TypedDict, Generic[EmojiNameT]):
    name: EmojiNameT
    id: EmojiNameT
    emotes: list[EmotePayload]


EmotesPayload = [EmojiUserPayload, EmotesDataPayload, EmotesDataPayload]
