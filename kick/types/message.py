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


class MessagePayload(TypedDict):
    id: str
    chatroom_id: int
    content: str
    type: Literal["message"]
    created_at: str
    sender: AuthorPayload


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
