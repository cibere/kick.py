from typing_extensions import TypedDict


class GiftEntryPayload(TypedDict):
    user_id: int
    username: str
    quantity: int


class LeaderboardPayload(TypedDict):
    gifts: list[GiftEntryPayload]
    gifts_week: list[GiftEntryPayload]
    gifts_month: list[GiftEntryPayload]
