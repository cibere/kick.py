from __future__ import annotations

from typing import TYPE_CHECKING

from .object import BaseDataclass
from .utils import cached_property

if TYPE_CHECKING:
    from .types.leaderboard import GiftEntryPayload, LeaderboardPayload
    from .user import User

__all__ = ("GiftLeaderboard", "GiftLeaderboardEntry")


class GiftLeaderboardEntry(BaseDataclass["GiftEntryPayload"]):
    @property
    def user_id(self) -> int:
        return self._data["user_id"]

    @property
    def quantity(self) -> int:
        return self._data["quantity"]

    @property
    def username(self) -> str:
        return self._data["username"]

    def __repr__(self) -> str:
        return f"<GiftLeaderboardEntry uid={self.user_id!r} quantity={self.quantity!r} username={self.username!r}>"


class GiftLeaderboard(BaseDataclass["LeaderboardPayload"]):
    streamer: User

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
