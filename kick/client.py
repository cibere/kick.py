from __future__ import annotations

import asyncio
import logging
from logging import getLogger
from typing import TYPE_CHECKING, Any, Callable, Coroutine, TypeVar

from .http import HTTPClient
from .message import Message
from .user import ClientUser, User
from .utils import MISSING, decorator, setup_logging

if TYPE_CHECKING:
    from typing_extensions import Self

    from .chatroom import Chatroom

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

    Attributes
    -----------
    user: ClientUser | None
        The user you are logged in as. It is `None` until `Client.login` is called.
    """

    def __init__(self, **options: Any) -> None:
        self._options = options
        self.http = HTTPClient(self)
        self._chatrooms: dict[int, Chatroom] = {}
        self.user: ClientUser | None = None

        LOGGER.warning(
            "Kick's api is undocumented, possible unstable, and can change at any time without warning"
        )

    def get_chatroom(self, chatroom_id: int, /) -> Chatroom | None:
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

        Examples
        -----------
        ```
            @client.event
            async def on_ready():
                print("The Bot is ready!")
        ```
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
        message: Message
            The message that was received
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
