from datetime import datetime, timedelta
from typing import Iterable

from account.models import User
from .models import Habit, RoundRecord, DailyRecord


class RecordSaver:
    @staticmethod
    def save(habit: Habit):
        if habit.is_due_or_done():
            __class__.__save_round_record_if_running(habit)
            __class__.__save_daily_record(habit)

    @staticmethod
    def __save_round_record_if_running(habit: Habit):
        if habit.is_running:
            round_record = RoundRecord()
            round_record.create_from_habit_running(habit)
            habit.end_recording(round_record.progress, save=False)

    @staticmethod
    def __save_daily_record(habit: Habit):
        # 어제 기록 저장
        daily_record = DailyRecord()
        daily_record.create_from_habit(habit)


class GoalAdjuster:
    @staticmethod
    def adjust_habit_goal(habit: Habit) -> None:
        if not habit.is_due_or_done():
            return

        if habit.growth_type == "INCREASE":
            growth_amount = habit.growth_amount
        elif habit.growth_type == "DECREASE":
            growth_amount = -habit.growth_amount

        # TODO: 해당 날짜 round record 있으면 됨.
        if habit.is_today_successful():
            # habit.goal_xp += growth_amount
            pass
        else:
            decrease_amount = int(habit.goal_xp * 0.1)
            habit.current_xp -= decrease_amount

            if habit.current_xp < 0:
                habit.goal_xp -= growth_amount
                decrease_amount = int(habit.goal_xp * 0.1)
                habit.current_xp = habit.goal_xp - decrease_amount


class DueAdjuster:
    @staticmethod
    def adjust_habit_due(habit: Habit) -> None:
        if habit.is_due_or_done():
            # 예정일이 아니었는데 진행한 경우, 원래는 None이라 오류 남
            # => 어제로 예정일을 바꿈
            user: User = habit.user
            habit.due_date = user.get_yesterday()
            habit.due_date += timedelta(days=habit.day_cycle)

    @staticmethod
    def set_is_today_due_date(habit: Habit):
        habit.is_today_due_date = __class__.is_today_due_date(habit)

    @staticmethod
    def is_today_due_date(habit: Habit):
        if habit.due_date == None:
            return False

        user: User = habit.user
        due_date_start = datetime.combine(habit.due_date, user.daily_reset_time)
        due_date_end = due_date_start + timedelta(days=1)

        now = datetime.now()
        if now < due_date_start:
            return False
        elif due_date_start <= now < due_date_end:
            return True
        elif due_date_end <= now:
            # 원래 예정일에 접속했더라면 알아서 다음 날로 갱신이 됨.
            # 이 경우는 예정일에 아예 접속조차 안 해서 갱신이 안 됐던 상황.
            # 밀린 게 쌓였을 수 있으므로, 부담을 줄이기 위해 예정에서 빼놓기
            return False
