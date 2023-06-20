from typing import Literal

from typing_extensions import TypedDict


class AuthorIdentity(TypedDict):
    color: str
    badges: list  # NEED TO FIGURE THIS OUT


class AuthorPayload(TypedDict):
    id: int
    username: str
    slug: str
    identity: AuthorIdentity


class MessagePayload(TypedDict):
    id: str
    chatroom_id: int
    content: str
    type: Literal["message"]
    created_at: str
    sender: AuthorPayload


class MessageStatusPayload(TypedDict):
    error: bool
    code: int
    message: str


class MessageSentPayload(TypedDict):
    status: MessageStatusPayload
    data: MessagePayload


class FetchMessagesDataPayload(TypedDict):
    messages: list[MessagePayload]
    cursor: str


class FetchMessagesPayload(TypedDict):
    status: MessageStatusPayload


class V1MessageSentPayload(TypedDict):
    status: int
    success: bool
    message: str
