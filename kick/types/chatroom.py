from codecs import StreamWriter

from typing_extensions import TypedDict

from .all import StatusPayload


class ChatroomRulesDataPayload(TypedDict):
    rules: str


class ChatroomRulesPayload(TypedDict):
    status: StatusPayload
    data: ChatroomRulesDataPayload


class DeletePollPayload(TypedDict):
    status: StatusPayload
    data: None


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


class BanChatterDataPayload(TypedDict):
    id: str
    chat_id: int
    banned_id: int
    banner_id: int
    reason: str
    type: str
    permanent: bool
    created_at: str
    expires_at: str


class BanChatterPayload(TypedDict):
    status: StatusPayload
    data: BanChatterDataPayload


class PollOptionPayload(TypedDict):
    id: int
    label: str
    votes: int


class PollPayload(TypedDict):
    title: str
    options: list[PollOptionPayload]
    duration: int
    remaining: int
    result_display_duration: int
    has_voted: bool


class CreatePollDataPayload(TypedDict):
    poll: PollPayload


class CreatePollPayload(TypedDict):
    status: StatusPayload
    data: CreatePollDataPayload


class ChatroomSettingPayload(TypedDict):
    enabled: bool


class FollowersModeStatusPayload(ChatroomSettingPayload):
    min_duration: int


class SlowModeStatusPayload(ChatroomSettingPayload):
    message_interval: int


class EditChatroomSettingsPayload(TypedDict):
    id: int
    slow_mode: SlowModeStatusPayload
    subscribers_mode: ChatroomSettingPayload
    followers_mode: FollowersModeStatusPayload
    emotes_mode: ChatroomSettingPayload
