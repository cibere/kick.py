from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .chatroom import ChatroomWebSocket
    from .http import HTTPClient


class State:
    def __init__(self, http: HTTPClient) -> None:
        self.http: HTTPClient = http
        self.ws: ChatroomWebSocket = http.ws
