from typing_extensions import TypedDict


class BannerImage1(TypedDict):
    url: str


class BannerImage2(TypedDict):
    src: str
    srcset: str


class InnerCategory(TypedDict):
    id: int
    name: str
    slug: str
    icon: str


class Category(TypedDict):
    id: int
    category_id: int
    name: str
    slug: str
    tags: list[str]
    description: str | None
    deleted_at: None  # NEED TO FIGURE THIS OUT
    category: InnerCategory


class Livestream(TypedDict):
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
    thumbnail: None  # NEED TO FIGURE THIS OUT
    categories: list[Category]
    tags: list  # NEED TO FIGURE THIS OUT


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


class SubscriberBadge(TypedDict):
    id: int
    channel_id: int
    months: int
    badge_image: BannerImage2


class UserPayload(TypedDict):
    id: int
    user_id: int
    slug: str
    is_banned: bool
    playback_url: str
    vod_enabled: bool
    subscription_enabled: bool
    cf_rate_limiter: str  # HOW DOES THIS WORK
    followers_count: int
    subscriber_badges: list[SubscriberBadge]
    banner_image: BannerImage1 | None
    role: None  # NEED TO FIGURE THIS OUT
    muted: bool
    follower_badges: list  # NEED TO FIGURE THIS OUT
    offline_banner_image: BannerImage2 | None
    verified: bool
    can_host: bool
    user: InnerUser
    chatroom: ChatroomPayload


class ChatterPayload(TypedDict):
    id: int
    username: str
    slug: str
    profile_pic: None  # NEED TO FIGURE THIS OUT
    is_staff: bool
    is_channel_owner: bool
    is_moderator: bool
    badges: list  # NEED TO FIGURE THIS OUT
    following_since: None  # NEED TO FIGURE THIS OUT
    susbribed_for: int  # NEED TO FIGURE THIS OUT
    banned: None  # NEED TO FIGURE THIS OUT
