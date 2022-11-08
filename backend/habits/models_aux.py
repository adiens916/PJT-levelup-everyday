from typing import Iterable
from .models import Habit, RoundRecord, DailyRecord


class RecordSaver:
    def __init__(self, habit_list: Iterable[Habit]) -> None:
        self.habit_list = habit_list

    def save(self):
        for habit in self.habit_list:
            if habit.is_due_or_done():
                self.__save_round_record_if_running(habit)
                self.__save_daily_record(habit)

    def __save_round_record_if_running(self, habit: Habit):
        if habit.is_running:
            round_record = RoundRecord()
            round_record.create_from_habit_running(habit)
            habit.add_progress_and_init(round_record.progress, save=False)

    def __save_daily_record(self, habit: Habit):
        # 어제 기록 저장
        daily_record = DailyRecord()
        daily_record.create_from_habit(habit)


class GoalAdjuster:
    pass


class DueAdjuster:
    pass
