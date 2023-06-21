from typing_extensions import TypedDict

from .all import StatusPayload


class ChatroomRulesDataPayload(TypedDict):
    rules: str


class ChatroomRulesPayload(TypedDict):
    status: StatusPayload
    data: ChatroomRulesDataPayload


class PollPayload(TypedDict):
    status: StatusPayload
    data: None  # NEED TO FIGURE THIS OUT


class ChatroomBannedWordsDataPayload(TypedDict):
    words: list[str]


class ChatroomBannedWordsPayload(TypedDict):
    status: StatusPayload
    data: ChatroomBannedWordsDataPayload


class BanEntryUserPayload(TypedDict):
    id: int
    username: str


class BanEntryDataPayload(TypedDict):
    reason: str
    banned_at: str
    permanent: bool
    expires_at: str


class BanEntryPayload(TypedDict):
    banned_user: BanEntryUserPayload
    banned_by: BanEntryUserPayload
    ban: BanEntryDataPayload


GetBannedUsersPayload = list[BanEntryPayload]


class UnbanChatterPayload(TypedDict):
    status: bool
    message: str
