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
