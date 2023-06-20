from typing import Literal

from typing_extensions import TypedDict

from .all import StatusPayload


class AuthorIdentity(TypedDict):
    color: str
    badges: list  # NEED TO FIGURE THIS OUT


class AuthorPayload(TypedDict):
    id: int
    username: str
    slug: str
    identity: AuthorIdentity


class BaseMessagePayload(TypedDict):
    id: str
    chatroom_id: int
    content: str
    created_at: str
    sender: AuthorPayload


class NormalMessagePayload(BaseMessagePayload):
    type: Literal["message"]


class ReplyOriginalSender(TypedDict):
    id: str
    username: str


class ReplyOriginalMessage(TypedDict):
    id: str
    content: str


class ReplyMetaData(TypedDict):
    original_sender: ReplyOriginalSender
    original_message: ReplyOriginalMessage


class ReplyMessagePayload(BaseMessagePayload):
    type: Literal["reply"]
    metadata: ReplyMetaData


MessagePayload = NormalMessagePayload | ReplyMessagePayload


class MessageSentPayload(TypedDict):
    status: StatusPayload
    data: MessagePayload


class FetchMessagesDataPayload(TypedDict):
    messages: list[MessagePayload]
    cursor: str


class FetchMessagesPayload(TypedDict):
    status: StatusPayload
    data: FetchMessagesDataPayload


class V1MessageSentPayload(StatusPayload):
    ...
