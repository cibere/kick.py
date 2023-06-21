from __future__ import annotations

import json
from datetime import datetime
from typing import TYPE_CHECKING, AsyncIterator

from aiohttp import ClientWebSocketResponse as WebSocketResponse

from .emotes import Emote
from .enums import ChatroomChatMode
from .message import Message
from .object import HTTPDataclass
from .polls import Poll
from .user import PartialUser
from .utils import cached_property

if TYPE_CHECKING:
    from .chatter import Chatter
    from .http import HTTPClient
    from .types.chatroom import BanEntryPayload
    from .types.user import ChatroomPayload
    from .user import User

__all__ = ("Chatroom", "BanEntry")


class ChatroomWebSocket:
    def __init__(self, ws: WebSocketResponse, *, http: HTTPClient):
        self.ws = ws
        self.http = http
        self.send_json = ws.send_json
        self.close = ws.close

    async def poll_event(self) -> None:
        raw_msg = await self.ws.receive()
        raw_data = raw_msg.json()
        msg = raw_data["data"]
        data = json.loads(msg)

        match raw_data["event"]:
            case "App\\Events\\ChatMessageEvent":
                msg = Message(data=data, http=self.http)
                self.http.client.dispatch("message", msg)

    async def start(self) -> None:
        while not self.ws.closed:
            await self.poll_event()

    async def subscribe(self, chatroom_id: int) -> None:
        await self.send_json(
            {
                "event": "pusher:subscribe",
                "data": {"auth": "", "channel": f"chatrooms.{chatroom_id}.v2"},
            }
        )

    async def unsubscribe(self, chatroom_id: int) -> None:
        await self.send_json(
            {
                "event": "pusher:unsubscribe",
                "data": {"auth": "", "channel": f"chatrooms.{chatroom_id}.v2"},
            }
        )


class BanEntry(HTTPDataclass["BanEntryPayload"]):
    chatroom: Chatroom

    @property
    def reason(self) -> str:
        return self._data["ban"]["reason"]

    @property
    def is_permanent(self) -> bool:
        return self._data["ban"]["permanent"]

    @cached_property
    def user(self) -> PartialUser:
        return PartialUser(data=self._data["banned_user"], http=self.http)

    @cached_property
    def banned_by(self) -> PartialUser:
        return PartialUser(data=self._data["banned_by"], http=self.http)

    @cached_property
    def banned_at(self) -> datetime:
        return datetime.fromisoformat(self._data["ban"]["banned_at"])

    @cached_property
    def expires_at(self) -> datetime | None:
        return (
            None
            if self.is_permanent is True
            else datetime.fromisoformat(self._data["ban"]["expires_at"])
        )

    async def unban(self) -> None:
        """
        |coro|

        Unbans the chatter from the chatroom.

        Raises
        -----------
        NotFound
            Streamer or chatter not found
        HTTPException
            Unbanning the chatter failed
        Forbidden
            You are unauthorized from unbanning the chatter
        """

        await self.http.unban_user(self.chatroom.streamer.username, self.user.username)


class Chatroom(HTTPDataclass["ChatroomPayload"]):
    streamer: User

    @property
    def id(self) -> int:
        return self._data["id"]

    @property
    def chatable_type(self) -> str:
        return self._data["chatable_type"]

    @cached_property
    def created_at(self) -> datetime:
        return datetime.fromisoformat(self._data["created_at"])

    @cached_property
    def updated_at(self) -> datetime:
        return datetime.fromisoformat(self._data["updated_at"])

    @property
    def chat_mode(self) -> ChatroomChatMode:
        return ChatroomChatMode(self._data["chat_mode"])

    @property
    def slowmode(self) -> bool:
        return self._data["slow_mode"]

    @property
    def followers_mode(self) -> bool:
        return self._data["followers_mode"]

    @property
    def subscribers_mode(self) -> bool:
        return self._data["subscribers_mode"]

    @property
    def emotes_mode(self) -> bool:
        return self._data["emotes_mode"]

    @property
    def message_interval(self) -> int:
        return self._data["message_interval"]

    @property
    def following_min_duration(self) -> int:
        return self._data["following_min_duration"]

    async def connect(self) -> None:
        """
        |coro|

        Connects to the chatroom, making it so you can now listen for the messages.
        """

        await self.http.ws.subscribe(self.id)
        self.http.client._chatrooms[self.id] = self

    async def disconnect(self) -> None:
        """
        |coro|

        disconnects to the chatroom, making it so you can no longer listen for the messages.
        """

        await self.http.ws.unsubscribe(self.id)
        self.http.client._chatrooms.pop(self.id)

    async def send(self, content: str, /) -> None:
        """
        |coro|

        Sends a message in the chatroom

        Parameters
        -----------
        content: str
            The message's content

        Raises
        -----------
        NotFound
            Streamer or chatter not found
        HTTPException
            Sending the message failed
        Forbidden
            You are unauthorized from sending the message
        """

        await self.http.send_message(self.id, content)

    async def fetch_chatter(self, chatter_name: str, /) -> Chatter:
        """
        |coro|

        Fetches a chatroom's chatter

        Parameters
        -----------
        chatter_name: str
            The chatter's username

        Raises
        -----------
        NotFound
            Streamer or chatter not found
        HTTPException
            Fetching the chatter failed

        Returns
        -----------
        Chatter
            The chatter
        """

        from .chatter import Chatter

        data = await self.http.get_chatter(self.streamer.slug, chatter_name)
        chatter = Chatter(data=data, http=self.http)
        chatter.chatroom = self
        return chatter

    async def fetch_rules(self) -> str:
        """
        |coro|

        Fetches the chatroom's rules

        Raises
        -----------
        NotFound
            Streamer Not Found
        HTTPException
            Fetching the rules failed

        Returns
        -----------
        str
            The rules
        """

        data = await self.http.get_chatroom_rules(self.streamer.slug)
        return data["data"]["rules"]

    async def fetch_banned_words(self) -> list[str]:
        """
        |coro|

        Fetches the chatroom's banned words

        Raises
        -----------
        NotFound
            Streamer Not Found
        HTTPException
            Fetching the words failed

        Returns
        -----------
        list[str]
            A list of the banned words
        """

        data = await self.http.get_channels_banned_words(self.streamer.slug)
        return data["data"]["words"]

    async def fetch_bans(self) -> AsyncIterator[BanEntry]:
        """
        |coro|

        Fetches the chatroom's bans

        Raises
        -----------
        NotFound
            Streamer Not Found
        HTTPException
            Fetching the bans failed

        Returns
        -----------
        AsyncIterator[BanEntry]
            Yields all of the ban entries
        """

        data = await self.http.get_channel_bans(self.streamer.slug)
        for entry_data in data:
            entry = BanEntry(data=entry_data, http=self.http)
            entry.chatroom = self
            yield entry

    async def fetch_poll(self) -> Poll:
        """
        |coro|

        Gets a poll from the chatroom

        Raises
        -----------
        NotFound
            There is no poll in the current chatroom or Streamer Not Found
        HTTPException
            Fetching the poll failed

        Returns
        -----------
        Poll
            The poll
        """

        data = await self.http.get_poll(self.streamer.slug)
        poll = Poll(data=data, http=self.http)
        poll.chatroom = self
        return poll

    async def fetch_emotes(
        self, *, include_global: bool = False
    ) -> AsyncIterator[Emote]:
        """
        |coro|

        Fetches the emotes from the current chatroom.

        Parameters
        -----------
        include_global: bool = False
            Wether to include global emotes or not

        Raises
        -----------
        NotFound
            Streamer Not Found
        HTTPException
            Fetching the bans failed

        Returns
        -----------
        AsyncIterator[Emote]
            Yields each emote. Starting with from the chatroom, then global
        """

        data = await self.http.get_emotes(self.streamer.slug)
        for emote in data[2]["emotes"]:
            yield Emote(data=emote, http=self.http)
        if include_global is True:
            for emote in data[1]["emotes"]:
                yield Emote(data=emote, http=self.http)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and other.id == self.id

    def __repr__(self) -> str:
        return f"<Chatroom id={self.id!r} streamer={self.streamer!r}>"
