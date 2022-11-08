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
    @staticmethod
    def adjust_habit_goal_by_success(habit: Habit, success: bool) -> None:
        if not habit.is_due_or_done():
            return

        if habit.growth_type == "INCREASE":
            growth_amount = habit.growth_amount
        elif habit.growth_type == "DECREASE":
            growth_amount = -habit.growth_amount

        if success:
            habit.goal_xp += growth_amount
        else:
            habit.goal_xp -= growth_amount

        habit.current_xp = 0


class DueAdjuster:

    # 예정일이 아니었는데 진행한 경우, 원래는 None이라 오류 남
    # => 어제로 예정일을 바꿈
    # self.due_date = self.user.get_yesterday()
    # self.due_date += timedelta(days=self.day_cycle)

    pass
