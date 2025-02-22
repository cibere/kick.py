from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, AsyncIterator, Optional

from .http import HTTPClient
from .message import Message

from .emotes import Emote
from .enums import ChatroomChatMode
from .object import HTTPDataclass
from .polls import Poll
from .users import PartialUser
from .utils import cached_property

if TYPE_CHECKING:
    from .chatter import Chatter
    from .types.chatroom import BanEntryPayload
    from .types.user import ChatroomPayload
    from .users import User

__all__ = ("Chatroom", "BanEntry", "PartialChatroom")


class BanEntry(HTTPDataclass["BanEntryPayload"]):
    """
    A dataclass which represents a ban entry on kick.
    This includes timeouts.

    Attributes
    -----------
    reason: str
        The reason for the ban/timeout
    is_permanent: bool
        Whether the ban is permanent. True == ban, false == timeout
    user: `PartialUser`
        The user the action was towards
    banned_by: `PartialUser`
        The responsible mod
    expires_at: datetime.datetime | None
        when the timeout expires at. None for a ban
    banned_at: datetime.datetime
        When the action happened
    chatroom: Chatroom
        The chatroom the action happened in
    """

    chatroom: Chatroom | PartialChatroom

    @property
    def reason(self) -> str:
        """
        The reason for the ban/timeout
        """

        return self._data["ban"]["reason"]

    @property
    def is_permanent(self) -> bool:
        """
        Whether the ban is permanent. True == ban, false == timeout
        """

        return self._data["ban"]["permanent"]

    @cached_property
    def user(self) -> PartialUser:
        """
        The user the action was towards
        """

        return PartialUser(
            id=self._data["banned_user"]["id"],
            username=self._data["banned_user"]["username"],
            http=self.http,
        )

    @cached_property
    def banned_by(self) -> PartialUser:
        """
        The responsible mod
        """

        return PartialUser(
            id=self._data["banned_by"]["id"],
            username=self._data["banned_by"]["username"],
            http=self.http,
        )

    @cached_property
    def banned_at(self) -> datetime:
        """
        When the action happened
        """

        return datetime.fromisoformat(self._data["ban"]["banned_at"])

    @cached_property
    def expires_at(self) -> datetime | None:
        """
        When the timeout expires at. None for a ban
        """

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

        await self.http.unban_user(self.chatroom.streamer_name, self.user.username)


class PartialChatroom:
    """
    A dataclass that represents a kick chatroom.

    Attributes
    -----------
    id: int
        The chatroom's id
    streamer: `User`
        The user who this chatroom belongs to
    """

    def __init__(self, *, id: int, streamer_name: str, http: HTTPClient) -> None:
        self.id = id
        self.streamer_name = streamer_name
        self.http = http

    async def connect(self) -> None:
        """
        |coro|

        Connects to the chatroom, making it so you can now listen for the messages.
        """

        await self.http.ws.subscribe_to_chatroom(self.id)
        self.http.client._chatrooms[self.id] = self

    async def disconnect(self) -> None:
        """
        |coro|

        Disconnects to the chatroom, making it so you can no longer listen for the messages.
        """

        await self.http.ws.unsubscribe_to_chatroom(self.id)
        self.http.client._chatrooms.pop(self.id)

    async def send(self, content: str, /) -> Message:
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

        Returns
        -----------
        Message
            The message
        """
        data = await self.http.send_message(self.id, content)
        message = Message(data=data["data"], http=self.http)
        return message

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

        data = await self.http.get_chatter(self.streamer_name, chatter_name)
        chatter = Chatter(data=data["data"], http=self.http, chatroom=self)
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

        data = await self.http.get_chatroom_rules(self.streamer_name)
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

        data = await self.http.get_channels_banned_words(self.streamer_name)
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

        data = await self.http.get_channel_bans(self.streamer_name)
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

        data = await self.http.get_poll(self.streamer_name)
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
            Whether to include global emotes or not

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

        data = await self.http.get_emotes(self.streamer_name)
        for emote in data[2]["emotes"]:
            yield Emote(data=emote, http=self.http)
        if include_global is True:
            for emote in data[1]["emotes"]:
                yield Emote(data=emote, http=self.http)


class Chatroom(PartialChatroom):
    """
    A dataclass that represents a kick chatroom.

    Attributes
    -----------
    id: int
        The chatroom's id
    chatable_type: str
        The chatroom's type
    created_at: datetime.datetime
        When the chatroom was created
    updated_at: datetime.datetime
        When the chatroom was last updated
    chat_mode: ChatroomChatMode
        The mode the chatroom is in
    slowmode: bool
        Whether slowmode is enabled
    followers_mode: bool
        Whether followers_mode is enabled
    subscribers_mode: bool
        Whether subscribers_mode is enabled
    emotes_mode: bool
        Whether emotes_mode is enabled
    slow_mode: bool
        Whether slow_mode is enabled
    message_interval: int
        Interval at which messages can be sent when slow_mode is enabled
    following_min_duration: int
        Unknown on what this is
    streamer: `User`
        The user who this chatroom belongs to
    """

    def __init__(self, *, data: ChatroomPayload, streamer: User, http: HTTPClient):
        super().__init__(id=data["id"], streamer_name=streamer.username, http=http)
        self._data = data
        self.streamer = streamer

    @property
    def chatable_type(self) -> str:
        """
        The chatroom's type
        """

        return self._data["chatable_type"]

    @cached_property
    def created_at(self) -> datetime:
        """
        When the chatroom was created
        """

        return datetime.fromisoformat(self._data["created_at"])

    @cached_property
    def updated_at(self) -> datetime:
        """
        When the chatroom was last updated
        """

        return datetime.fromisoformat(self._data["updated_at"])

    @property
    def chat_mode(self) -> ChatroomChatMode:
        """
        The mode the chatroom is in
        """

        return ChatroomChatMode(self._data["chat_mode"])

    @property
    def slowmode(self) -> bool:
        """
        Whether slowmode is enabled
        """

        return self._data["slow_mode"]

    @property
    def followers_mode(self) -> bool:
        """
        Whether followers_mode is enabled
        """

        return self._data["followers_mode"]

    @property
    def subscribers_mode(self) -> bool:
        """
        Whether subscribers_mode is enabled
        """

        return self._data["subscribers_mode"]

    @property
    def emotes_mode(self) -> bool:
        """
        Whether emotes_mode is enabled
        """

        return self._data["emotes_mode"]

    @property
    def slow_mode(self) -> bool:
        """
        Whether slow_mode is enabled
        """

        return self._data["slow_mode"]

    @property
    def message_interval(self) -> int:
        """
        Interval at which messages can be sent when slow_mode is enabled
        """

        return self._data["message_interval"]

    @property
    def following_min_duration(self) -> int:
        """
        Unknown on what this is
        """

        return self._data["following_min_duration"]

    async def edit(
        self,
        *,
        followers_only_mode: Optional[bool] = None,
        emotes_only_mode: Optional[bool] = None,
        subscribers_only_mode: Optional[bool] = None,
        slow_mode_enabled: Optional[bool] = None,
        slow_mode_interval: Optional[int] = None,
    ) -> None:
        """
        |coro|

        Edits the chatroom's settings

        Parameters
        -----------
        followers_only_mode: Optional[bool] = None
            Lets you enable/disable followers only mode.
        emotes_only_mode: Optional[bool] = None
            Lets you enable/disable emotes only mode.
        subscribers_only_mode: Optional[bool] = None
            Lets you enable/disable subscribers only mode.
        slow_mode_enabled: Optional[bool] = None
            Lets you enable/disable slow_mode only mode.
        slow_mode_interval: Optional[int] = None
            Lets you set the slow mode interval

        Raises
        -----------
        `NotFound`
            Streamer not found
        `HTTPException`
            Editing the chatroom failed
        `Forbidden`
            You are unauthorized from editing the chatroom.
        """

        streamer_name = self.streamer_name

        payload = {}
        if self.followers_mode is not None:
            payload["followers_mode"] = self.followers_mode

        if self.emotes_mode is not None:
            payload["emotes_mode"] = self.emotes_mode

        if self.subscribers_mode is not None:
            payload["subscribers_mode"] = self.subscribers_mode

        if self.slow_mode is not None:
            payload["slow_mode"] = self.slow_mode
            if self.slow_mode and self.message_interval is not None:
                payload["message_interval"] = self.message_interval

        if not payload:
            raise ValueError("No valid parameters provided for chatroom editing.")

        await self.http.edit_chatroom(streamer_name, payload)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and other.id == self.id

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id!r} streamer={self.streamer_name!r}>"
