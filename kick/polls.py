from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Iterator

from .object import HTTPDataclass
from .utils import cached_property

if TYPE_CHECKING:
    from .chatroom import Chatroom
    from .types.chatroom import CreatePollPayload, PollOptionPayload

__all__ = ("PollOption", "Poll")


class PollOption(HTTPDataclass["PollOptionPayload"]):
    """
    This dataclass represents a chatroom `Poll`'s option on kick.

    Attributes
    -----------
    chatroom: `Chatroom`
        The chatroom the poll is in
    id: int
        The option's id
    label: str
        The option's label
    votes: int
        The amount of votes the option has
    """

    chatroom: Chatroom

    @property
    def id(self) -> int:
        """
        The option's id
        """

        return self._data["id"]

    @property
    def label(self) -> str:
        """
        The option's label
        """

        return self._data["label"]

    @property
    def votes(self) -> int:
        """
        The amount of votes the option has
        """

        return self._data["votes"]

    async def vote(self) -> None:
        """
        |coro|

        Votes for this option in the poll

        Raises
        -----------
        NotFound
            There is no poll in the current chatroom
        HTTPException
            Deleting the poll failed
        """

        await self.http.vote_for_poll(self.chatroom.streamer.slug, self.id)


class Poll(HTTPDataclass["CreatePollPayload"]):
    """
    This dataclass represents a poll in a chatroom on kick.

    Attributes
    -----------
    chatroom: `Chatroom`
        The chatroom the poll is in
    title: str
        The poll's title
    options: list[`PollOption`]
        The poll's options
    duration: int
        How long the poll will last in seconds
    result_display_duration: int
        How long the poll will display the results in seconds
    has_voted: bool
        if you've voted yet
    ends_at: datetime.datetime
        When the poll ends at
    """

    chatroom: Chatroom

    @property
    def title(self) -> str:
        """
        Gives you the poll's title
        """

        return self._data["data"]["poll"]["title"]

    def _get_options(self) -> Iterator[PollOption]:
        for entry in self._data["data"]["poll"]["options"]:
            option = PollOption(data=entry, http=self.http)
            option.chatroom = self.chatroom
            yield option

    @cached_property
    def options(self) -> list[PollOption]:
        """
        The poll's options
        """

        return list(self._get_options())

    @property
    def duration(self) -> int:
        """
        How long the poll is set to last in seconds
        """

        return self._data["data"]["poll"]["duration"]

    @property
    def result_display_duration(self) -> int:
        """
        How long the poll will be displayed after it ends, in seconds
        """

        return self._data["data"]["poll"]["result_display_duration"]

    @property
    def has_voted(self) -> bool:
        """
        Returns if you've voted yet
        """

        return self._data["data"]["poll"]["has_voted"]

    @cached_property
    def ends_at(self) -> datetime.datetime:
        """
        How long the poll is set to last in seconds
        """

        now = datetime.datetime.now(datetime.UTC)
        return now + datetime.timedelta(seconds=self._data["data"]["poll"]["remaining"])

    async def delete(self) -> None:
        """
        |coro|

        Deletes the current poll from the chatroom

        Raises
        -----------
        Forbidden
            You are unauthorized to delete the poll
        NotFound
            There is no poll in the current chatroom
        HTTPException
            Deleting the poll failed
        """

        await self.http.delete_poll(self.chatroom.streamer.slug)
