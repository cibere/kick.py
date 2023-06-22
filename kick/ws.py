from __future__ import annotations

import json
from typing import TYPE_CHECKING

from aiohttp import ClientWebSocketResponse as WebSocketResponse

from .livestream import PartialLivestream
from .message import Message

if TYPE_CHECKING:
    from .http import HTTPClient

__all__ = ()


class PusherWebSocket:
    def __init__(self, ws: WebSocketResponse, *, http: HTTPClient):
        self.ws = ws
        self.http = http
        self.send_json = ws.send_json
        self.close = ws.close

    async def poll_event(self) -> None:
        raw_msg = await self.ws.receive()
        raw_data = raw_msg.json()
        data = json.loads(raw_data["data"])

        self.http.client.dispatch("payload_receive", raw_data["event"], data)
        self.http.client.dispatch("raw_payload_receive", raw_data)

        match raw_data["event"]:
            case "App\\Events\\ChatMessageEvent":
                msg = Message(data=data, http=self.http)
                self.http.client.dispatch("message", msg)
            case "App\\Events\\StreamerIsLive":
                livestream = PartialLivestream(data=data, http=self.http)
                self.http.client.dispatch("livestream_start", livestream)
            case "App\\Events\\FollowersUpdated":
                user = self.http.client._watched_users[data["channel_id"]]
                if data["followed"] is True:
                    event = "follow"
                    user._data["followers_count"] += 1
                else:
                    event = "unfollow"
                    user._data["followers_count"] -= 1

                self.http.client.dispatch(event, user)

    async def start(self) -> None:
        while not self.ws.closed:
            await self.poll_event()

    async def subscribe_to_chatroom(self, chatroom_id: int) -> None:
        await self.send_json(
            {
                "event": "pusher:subscribe",
                "data": {"auth": "", "channel": f"chatrooms.{chatroom_id}.v2"},
            }
        )

    async def unsubscribe_to_chatroom(self, chatroom_id: int) -> None:
        await self.send_json(
            {
                "event": "pusher:unsubscribe",
                "data": {"auth": "", "channel": f"chatrooms.{chatroom_id}.v2"},
            }
        )

    async def watch_channel(self, channel_id: int) -> None:
        await self.send_json(
            {
                "event": "pusher:subscribe",
                "data": {"auth": "", "channel": f"channel.{channel_id}"},
            }
        )

    async def unwatch_channel(self, channel_id: int) -> None:
        await self.send_json(
            {
                "event": "pusher:subscribe",
                "data": {"auth": "", "channel": f"channel.{channel_id}"},
            }
        )
