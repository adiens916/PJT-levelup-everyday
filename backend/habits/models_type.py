from typing import TypedDict


class DailyRecordType(TypedDict):
    habit: int
    date: str
    success: bool
    level_now: int
    level_change: int
    xp_now: int
    xp_change: int
