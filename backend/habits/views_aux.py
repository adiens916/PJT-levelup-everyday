import json
from datetime import datetime, timedelta
from typing import Iterable

from django.core import serializers
from django.db.models import Model
from django.http import JsonResponse

from account.models import User
from .models import DailyRecord, Habit, RoundRecord
from .tests import is_day_changed, is_due_today


def json_response_wrapper(queryset: Iterable[Model]):
    queryset_json = serializers.serialize("json", queryset, ensure_ascii=False)
    queryset_dict = json.loads(queryset_json)
    return JsonResponse(queryset_dict, safe=False)


def is_day_changed_for_user(user: User):
    return is_day_changed(user.next_reset_date, user.daily_reset_time, datetime.now())


def is_due_today_for_habit(habit: Habit):
    user: User = habit.user
    return is_due_today(habit.due_date, user.daily_reset_time, datetime.now())


def update_goals_and_due_dates(habit_list: Iterable[Habit], user: User):
    """
    오늘이 예정일인 경우,
    이전의 성공/실패 여부를 참고해
    오늘 목표를 조정한다.
    """

    for habit in habit_list:
        if habit.is_due_or_done():
            habit.save_round_record_if_running()

            # 어제 기록 저장
            daily_record = DailyRecord()
            daily_record.save_from_habit(habit)

            # 어제 기록에 따라 목표 조정
            habit.adjust_goal_and_due_date_by_success(daily_record.success)

        # 오늘 해야 하는지
        habit.set_is_today_due_date()
        habit.save()

    # Habit.objects.bulk_update(habit_list, [''])
