from typing import Any

from typing_extensions import TypedDict


class ClientChatterPayload(TypedDict):
    subscription: None  # NEED TO FIGURE THIS OUT
    is_super_admin: bool
    is_following: bool
    following_since: None | str
    is_broadcaster: bool
    is_moderator: bool
    leaderboards: Any  # NEED TO FIGURE THIS OUT
    banned: None  # NEED TO FIGURE THIS OUT


class ChatterPayload(TypedDict):
    id: int
    username: str
    slug: str
    profile_pic: str
    is_staf: bool
    is_channel_owner: bool
    is_moderator: bool
    badges: list  # NEED TO FIGURE THIS OUT
    following_since: None | str
    subscribed_for: int  # NEED TO FIGURE THIS OUT
    banned: None  # NEED TO FIGURE THIS OUT
