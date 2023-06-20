from typing import Literal

from typing_extensions import TypedDict

from .user import InnerUser


class EmotePayload(TypedDict):
    id: int
    channel_id: int
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
    emotes: list[EmotePayload]
    can_host: bool
    user: InnerUser


class EmotesDataPayload(TypedDict):
    emotes: list[EmotePayload]


class GlobalEmotesPayload(EmotesDataPayload):
    name: Literal["Global"]
    id: Literal["Global"]


class StreamerEmotesPayload(EmotesDataPayload):
    name: Literal["Emojis"]
    id: Literal["Emoji"]


EmotesPayload = tuple[EmojiUserPayload, GlobalEmotesPayload, StreamerEmotesPayload]
