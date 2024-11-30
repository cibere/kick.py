from __future__ import annotations

import asyncio
import logging
from logging import getLogger
from typing import TYPE_CHECKING, Any, Callable, Coroutine, TypeVar

from .chatroom import Chatroom, PartialChatroom
from .chatter import PartialChatter
from .http import HTTPClient
from .livestream import PartialLivestream
from .message import Message
from .users import ClientUser, PartialUser, User, StreamInfo, DestinationInfo
from .categories import CategorySearchResult
from .utils import MISSING, decorator, setup_logging

if TYPE_CHECKING:
    from typing_extensions import Self
    from .categories import CategorySearchResult

EventT = TypeVar("EventT", bound=Callable[..., Coroutine[Any, Any, None]])
LOGGER = getLogger(__name__)

__all__ = ("Credentials", "Client")


class Credentials:
    """
    This holds credentials that can be used to authenticate yourself with kick.

    Parameters
    -----------
    username: Optional[str]
        The username to login with. Can not be used with the `email` arg
    email: Optional[str]
        The email to login with. Can not be used with the `username` arg
    password: str
        The account's password
    one_time_password: Optional[str]
        The 2FA code to login with

    Attributes
    -----------
    username: Optional[str]
        The username to login with. Can not be used with the `email` arg
    email: Optional[str]
        The email to login with. Can not be used with the `username` arg
    password: str
        The account's password
    one_time_password: Optional[str]
        The 2FA code to login with
    """

    def __init__(
        self,
        *,
        username: str = MISSING,
        email: str = MISSING,
        password: str,
        one_time_password: str | None = None,
    ) -> None:
        if username is MISSING and email is MISSING:
            raise ValueError("Provide either a `username` or `email` arg")
        elif username is not MISSING and email is not MISSING:
            raise ValueError("Provide `username` or `email`, not both.")

        self.email: str = username or email
        self.username_was_provided: bool = username is not MISSING
        self.password: str = password
        self.one_time_password: str | None = one_time_password


class Client:
    """
    This repersents the Client you can use to interact with kick.

    Parameters
    -----------
    **options: Any
        Options that can be passed

    Options
    -----------
    whitelisted: bool = False
        If you have been api whitelisted. If set to True, the bypass script will not be used.
    bypass_port: int = 9090
        The port the bypass script is running on. Defaults to 9090
    bypass_host: str = "http://localhost"
        The host of the bypass script.

    Attributes
    -----------
    user: ClientUser | None
        The user you are logged in as. It is `None` until `Client.login` is called.
    """

    def __init__(self, **options: Any) -> None:
        self._options = options
        self.http = HTTPClient(self)
        self._chatrooms: dict[int, Chatroom | PartialChatroom] = {}
        self._watched_users: dict[int, User] = {}
        self.user: ClientUser | None = None

        LOGGER.warning(
            "Kick's api is undocumented, possible unstable, and can change at any time without warning"
        )

    def get_partial_chatroom(
        self, chatroom_id: int, streamer_name: str
    ) -> PartialChatroom:
        """
        Gets a partial chatroom.

        Parameters
        -----------
        chatroom_id: int
            The id of the chatroom you want to connect to
        streamer_name: str
            The name of the streamer who's chatroom it is

        Returns
        -----------
        `PartialChatroom`
            The partial chatroom
        """

        return PartialChatroom(
            id=chatroom_id, streamer_name=streamer_name, http=self.http
        )

    def get_chatroom(self, chatroom_id: int, /) -> PartialChatroom | Chatroom | None:
        """
        Gets a chatroom out of a cache that contains chatrooms that you are connected to.

        Parameters
        -----------
        chatroom_id: int
            The chatroom's id

        Returns
        -----------
        Chatroom | None
            Either the chatroom, or None
        """

        return self._chatrooms.get(chatroom_id)

    def get_partial_user(self, *, username: str, id: int) -> PartialUser:
        """
        Gets a partial user instance by the username and id provided.

        Parameters
        -----------
        username: str
            The user's name
        id: int
            The user's id

        Returns
        -----------
        `PartialUser`
            The partial user
        """

        return PartialUser(username=username, id=id, http=self.http)

    def get_partial_chatter(
        self, *, streamer_name: str, chatter_name: str
    ) -> PartialChatter:
        """
        Gets a partial chatter instance by the streamer and chatter names provided.

        Parameters
        -----------
        streamer_name: str
            The streamer's username or slug
        chatter_name: str
            The chatter's username or slug

        Returns
        -----------
        `PartialChatter`
            The partial chatter
        """

        return PartialChatter(
            streamer_name=streamer_name, chatter_name=chatter_name, http=self.http
        )

    async def fetch_user(self, name: str, /) -> User:
        """
        |coro|

        Fetches a user from the API.

        Parameters
        -----------
        name: str
            The user's slug or username

        Raises
        -----------
        HTTPException
            Fetching Failed
        NotFound
            No user with the username/slug exists

        Returns
        -----------
        User
            The user object associated with the streamer
        """

        data = await self.http.get_user(name)
        user = User(data=data, http=self.http)
        return user

    async def fetch_stream_url_and_key(self) -> DestinationInfo:
        """
        |coro|
        Fetches your stream URL and stream key from the API.
        You must be authenticated to use this endpoint.
        Raises
        -----------
        HTTPException
            Fetching Failed
        Forbidden
            You are not authenticated
        Returns
        -----------
        DestinationInfo
        """

        data = await self.http.fetch_stream_destination_url_and_key()
        return DestinationInfo(data=data)

    async def set_stream_info(
        self,
        title: str,
        language: str,
        subcategory_id: int,
        subcategory_name: str | None = None,
        is_mature: bool = False,
    ) -> StreamInfo:
        """
        |coro|
        Updates the stream information.
        Parameters
        -----------
        title: str
            The new stream title
        language: str
            The stream language (e.g. "English")
        subcategory_id: int
            The ID of the game/category
        subcategory_name: Optional[str]
            The name of the game/category (optional)
        is_mature: bool
            Whether the stream is marked as mature content
        Raises
        -----------
        HTTPException
            Failed to update stream information
        """

        data = await self.http.set_stream_info(title, subcategory_name, subcategory_id, language, is_mature)
        return StreamInfo(data=data)

    async def search_categories(self, query: str, /) -> CategorySearchResult:
        """
        |coro|

        Searches for categories/games on Kick.

        Parameters
        -----------
        query: str
            The search query string

        Raises
        -----------
        HTTPException
            Search request failed

        Returns
        -----------
        SearchResponse
            The search results containing matching categories
        """

        data = await self.http.search_categories(query)
        return CategorySearchResult(data=data)

    def dispatch(self, event_name: str, *args, **kwargs) -> None:
        event_name = f"on_{event_name}"

        event = getattr(self, event_name, None)
        if event is not None:
            asyncio.create_task(
                event(*args, **kwargs), name=f"event-dispatch: {event_name}"
            )

    @decorator
    def event(self, coro: EventT) -> EventT:
        """
        Lets you set an event outside of a subclass.
        """

        setattr(self, coro.__name__, coro)
        return coro

    async def login(self, credentials: Credentials) -> None:
        """
        |coro|

        Authenticates yourself, and fills `Client.user`
        Unlike `Client.start`, this does not start the websocket

        Parameters
        -----------
        credentials: Credentials
            The credentials to authenticate yourself with
        """

        await self.http.login(credentials)

        data = await self.http.get_me()
        self.user = ClientUser(data=data, http=self.http)

    async def start(self, credentials: Credentials | None = None) -> None:
        """
        |coro|

        Starts the websocket so you can receive events
        And authenticate yourself if credentials are provided.

        Parameters
        -----------
        credentials: Optional[Credentials]
            The credentials to authenticate yourself with, if any
        """

        if credentials is not None:
            await self.login(credentials)
        await self.http.start()

    async def close(self) -> None:
        """
        |coro|

        Closes the HTTPClient, no requests can be made after this.
        """

        await self.http.close()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    async def on_ready(self) -> None:
        """
        |coro|

        on_ready is an event that can be overriden with the `Client.event` decorator or with a subclass.
        This is called after the client has started the websocket and is receiving events.
        """

    async def on_message(self, message: Message) -> None:
        """
        |coro|

        on_ready is an event that can be overriden with the `Client.event` decorator or with a subclass.
        This is called when a message is received over the websocket

        Parameters
        -----------
        message: `Message`
            The message that was received
        """

    async def on_payload_receive(self, event: str, payload: dict) -> None:
        """
        |coro|

        on_payload_receive is an event that can be overriden with the `Client.event` decorator or with a subclass.
        This is called when an event is received from the websocket.

        Parameters
        -----------
        event: str
            The payload's event
        payload: dict
            The payload
        """

    async def on_livestream_start(self, livestream: PartialLivestream) -> None:
        """
        |coro|

        on_livestream_start is an event that can be overriden with the `Client.event` decorator or with a subclass.
        This is called when a user that is being watched starts streaming

        Parameters
        -----------
        livestream: `PartialLivestream`
            The livestream
        """

    async def on_follow(self, streamer: User) -> None:
        """
        |coro|

        on_livestream_start is an event that can be overriden with the `Client.event` decorator or with a subclass.
        This is called when someone starts following a streamer that is being watched.

        Parameters
        -----------
        streamer: `User`
            The streamer
        """

    async def on_unfollow(self, streamer: User) -> None:
        """
        |coro|

        on_livestream_start is an event that can be overriden with the `Client.event` decorator or with a subclass.
        This is called when someone stops following a streamer that is being watched.

        Parameters
        -----------
        streamer: `PartialLivestream`
            The streamer
        """

    def run(
        self,
        credentials: Credentials | None = None,
        *,
        handler: logging.Handler = MISSING,
        formatter: logging.Formatter = MISSING,
        level: int = MISSING,
        root: bool = True,
        stream_supports_colour: bool = False,
    ) -> None:
        """
        Starts the websocket so you can receive events
        And authenticate yourself if credentials are provided.

        `Client.run` automatically calls `utils.setup_logging` with the provided kwargs, and calls `Client.start`.

        Parameters
        -----------
        credentials: Optional[Credentials]
            The credentials to authenticate yourself with, if any
        """

        setup_logging(
            handler=handler,
            formatter=formatter,
            level=level,
            root=root,
            stream_supports_colour=stream_supports_colour,
        )
        asyncio.run(self.start(credentials))
