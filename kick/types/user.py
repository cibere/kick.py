from typing_extensions import Any, TypedDict, Optional

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
    role: None  # Unknown
    muted: bool
    follower_badges: list  # Unknown
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
    banned: None  # Unknown


class ClientChatterPayload(TypedDict):
    subscription: None  # Unknown
    is_super_admin: bool
    is_following: bool
    following_since: None | str
    is_broadcaster: bool
    is_moderator: bool
    leaderboards: Any  # Unknown
    banned: None  # Unknown


class PartialUserPayload(TypedDict):
    id: str | int
    username: str


class ClientUserStreamerChannelsPayload(TypedDict):
    id: int
    user_id: int
    slug: str
    is_banned: bool
    playback_url: None | str
    name_updated_at: None  # Unknown
    vod_enabled: bool
    subscription_enabled: bool
    can_host: bool
    verified: None  # Unknown


class StreamInfoPayload(TypedDict):
    title: str
    subcategoryId: int
    subcategoryName: Optional[str]
    language: str
    is_mature: bool


class ClientUserPayload(TypedDict):
    id: int
    email: str
    username: str
    google_id: None  # Unknown
    agreed_to_terms: bool
    email_verified_at: str
    bio: None | str
    country: None | str
    state: None | str
    city: None | str
    enable_live_notifications: bool
    youtube: None | str
    instagram: None | str
    twitter: None | str
    discord: None | str
    tiktok: None | str
    facebook: None | str
    enable_onscreen_live_notifications: bool
    apple_id: None  # Unknown
    phone: None | int
    email_updated_at: None  # Unknown
    newsletter_subscribed: bool
    enable_sms_promo: bool
    enable_sms_security: bool
    is_2fa_setup: bool
    redirect: None  # Unknown
    channel_can_be_updated: bool
    is_live: bool
    intercom_hash: None  # Unknown
    streamer_channel: ClientUserStreamerChannelsPayload
    roles: list  # Unknown
    profilepic: str | None
