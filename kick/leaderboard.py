from __future__ import annotations

from typing import TYPE_CHECKING

from .object import BaseDataclass
from .utils import cached_property

if TYPE_CHECKING:
    from .types.leaderboard import GiftEntryPayload, LeaderboardPayload
    from .users import AnyUser

__all__ = ("GiftLeaderboard", "GiftLeaderboardEntry")


class GiftLeaderboardEntry(BaseDataclass["GiftEntryPayload"]):
    """
    This dataclass represents a gift leaderboard entry.

    Attributes
    -----------
    user_id: int
        The id of the user with this entry
    quantity: int
        The amount of subs this person has gifted
    username: str
        The user's username
    """

    @property
    def user_id(self) -> int:
        """
        The id of the user with this entry
        """

        return self._data["user_id"]

    @property
    def quantity(self) -> int:
        """
        The amount of subs this person has gifted
        """

        return self._data["quantity"]

    @property
    def username(self) -> str:
        """
        The user's username
        """

        return self._data["username"]

    def __repr__(self) -> str:
        return f"<GiftLeaderboardEntry uid={self.user_id!r} quantity={self.quantity!r} username={self.username!r}>"


class GiftLeaderboard(BaseDataclass["LeaderboardPayload"]):
    """
    This is a dataclass which reprsents the gift leaderboard for a kick streamer.

    Attributes
    -----------
    streamer: `User`
        The streamer that the leaderboard is for
    this_week: list[`GiftLeaderboardEntry`]
        The gift leaderboard for the current week
    this_month: list[`GiftLeaderboardEntry`]
        The gift leaderboard for the current month
    all_time: list[`GiftLeaderboardEntry`]
        The gift leaderboard for all time
    """

    streamer: AnyUser

    @cached_property
    def this_week(self) -> list[GiftLeaderboardEntry]:
        return [GiftLeaderboardEntry(data=c) for c in self._data["gifts_week"]]

    @cached_property
    def this_month(self) -> list[GiftLeaderboardEntry]:
        return [GiftLeaderboardEntry(data=c) for c in self._data["gifts_month"]]

    @cached_property
    def all_time(self) -> list[GiftLeaderboardEntry]:
        return [GiftLeaderboardEntry(data=c) for c in self._data["gifts"]]

    def __repr__(self) -> str:
        return f"<GiftLeaderboard streamer={self.streamer.username!r} weekly_entries={len(self.this_week)} monthly_entries={len(self.this_month)} all_time_etries={len(self.all_time)}>"
