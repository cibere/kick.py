from typing_extensions import TypedDict


class StatusPayload(TypedDict):
    error: bool
    code: int
    message: str
