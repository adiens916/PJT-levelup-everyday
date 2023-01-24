from typing import TypedDict, Literal


class HabitCreateType(TypedDict):
    name: str
    description: str
    estimate_type: Literal["TIME", "COUNT"]
    estimate_unit: str
    final_goal: int
    growth_type: Literal["INCREASE", "DECREASE"]
    day_cycle: int
    importance: str
    initial_goal: int


class HabitReadType(HabitCreateType):
    """extending HabitCreateType"""

    level: int
    goal_xp: int
    current_xp: int
    growth_amount: int
    due_date: str
    is_today_due_date: bool
    is_done: bool

    is_running: bool
    start_datetime: str
    is_paused: bool
    paused_datetime: str
    temporary_progress: int


class DailyRecordType(TypedDict):
    habit: int
    date: str
    success: bool
    level_now: int
    level_change: int
    xp_change: int
    xp_accumulate: int
