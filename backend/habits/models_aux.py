from datetime import date, datetime, timedelta
from django.shortcuts import get_object_or_404

from account.models import User
from .models import Habit, RoundRecord, DailyRecord


class RecordSaver:
    @staticmethod
    def save(habit: Habit):
        if habit.is_due_or_done() and habit.is_running:
            round_record = RoundRecord()
            round_record.create_from_habit_running(habit)
            habit.end_recording(round_record.progress, save=False)

            daily_record = get_object_or_404(
                DailyRecord, habit=habit.pk, date=date.today()
            )
            daily_record.create_from_habit(habit)


class GoalAdjuster:
    @staticmethod
    def adjust_habit_goal(habit: Habit) -> None:
        if habit.is_done:
            habit.use_xp_for_level_up()
        elif habit.is_today_due_date:
            habit.lose_xp()
        else:
            return


class DueAdjuster:
    @staticmethod
    def adjust_habit_due(habit: Habit) -> None:
        if habit.is_due_or_done():
            user: User = habit.user
            # due date will be reset as yesterday
            # on which the user did the habit actually
            habit.due_date = user.get_yesterday()
            habit.due_date += timedelta(days=habit.day_cycle)
            habit.is_done = False

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
