from typing import Iterable
from .models import Habit, RoundRecord, DailyRecord


class RecordSaver:
    def __init__(self, habit_list: Iterable[Habit]) -> None:
        self.habit_list = habit_list

    def save(self):
        for habit in self.habit_list:
            if habit.is_due_or_done():
                self.save_round_record_if_running(habit)
                self.save_daily_record(habit)

    def save_round_record_if_running(self, habit: Habit):
        # 1. 저장
        habit.save_round_record_if_running()

    def save_daily_record(self, habit: Habit):
        # 어제 기록 저장
        daily_record = DailyRecord()
        daily_record.create_from_habit(habit)


class GoalAdjuster:
    pass


class DueAdjuster:
    pass
