from typing_extensions import Any, TypedDict

from .assets import AssetSrcset, AssetUrl
from .badges import ChatBadgePayload, SubscriberBadgePayload
from .categories import Category
from .videos import LivestreamPayload


class InnerUser(TypedDict):
    id: int
    username: str
    agreed_to_terms: bool
    email_verified_at: str
    bio: str
    country: str
    state: str
    city: str
    instagram: str
    twitter: str
    youtube: str
    discord: str
    tiktok: str
    facebook: str
    profile_pic: str


class ChatroomPayload(TypedDict):
    id: int
    chatable_type: str
    channel_id: int
    created_at: str
    updated_at: str
    chat_mode_old: str
    chat_mode: str
    slow_mode: bool
    chatable_id: int
    followers_mode: bool
    subscribers_mode: bool
    emotes_mode: bool
    message_interval: int
    following_min_duration: int


class UserPayload(TypedDict):
    id: int
    user_id: int
    slug: str
    is_banned: bool
    playback_url: str
    vod_enabled: bool
    subscription_enabled: bool
    followers_count: int
    subscriber_badges: list[SubscriberBadgePayload]
    banner_image: AssetUrl | None
    role: None  # NEED TO FIGURE THIS OUT
    muted: bool
    follower_badges: list  # NEED TO FIGURE THIS OUT
    offline_banner_image: AssetSrcset | None
    verified: bool
    can_host: bool
    user: InnerUser
    chatroom: ChatroomPayload
    livestream: LivestreamPayload | None
    recent_categories: list[Category]


class ChatterPayload(TypedDict):
    id: int
    username: str
    slug: str
    profile_pic: None | str
    is_staff: bool
    is_channel_owner: bool
    is_moderator: bool
    badges: list[ChatBadgePayload]
    following_since: None | str
    subscribed_for: int  # in months
    banned: None  # NEED TO FIGURE THIS OUT


class ClientChatterPayload(TypedDict):
    subscription: None  # NEED TO FIGURE THIS OUT
    is_super_admin: bool
    is_following: bool
    following_since: None | str
    is_broadcaster: bool
    is_moderator: bool
    leaderboards: Any  # NEED TO FIGURE THIS OUT
    banned: None  # NEED TO FIGURE THIS OUT


class PartialUserPayload(TypedDict):
    id: str | int
    username: str
