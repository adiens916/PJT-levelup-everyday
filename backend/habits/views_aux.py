import json
from datetime import datetime, time, timedelta
from typing import Iterable

from django.core import serializers
from django.db.models import Model
from django.http import JsonResponse

from account.models import User
from .models import DailyRecord, Habit, RoundRecord
from .tests import is_day_changed, is_due_today


def json_response_wrapper(queryset: Iterable[Model]):
    queryset_json = serializers.serialize('json', queryset, ensure_ascii=False)
    queryset_dict = json.loads(queryset_json)
    return JsonResponse(queryset_dict, safe=False)


def is_day_changed_for_user(user: User):
    return is_day_changed(
        user.next_reset_date, 
        user.daily_reset_time, 
        datetime.now()
    )


def is_due_today_for_habit(habit: Habit):
    return is_due_today(
        habit.due_date, 
        habit.day_cycle, 
        datetime.now()
    )


def update_goals_and_due_dates(habit_list: Iterable[Habit], user: User):
    '''
    오늘이 예정일인 경우,
    이전의 성공/실패 여부를 참고해
    오늘 목표를 조정한다.
    '''

    reset_date = datetime.combine(datetime.now().date(), user.daily_reset_time)
    just_a_minute_ago = reset_date - timedelta(minutes=1)
    yesterday = reset_date - timedelta(days=1)

    for habit in habit_list:
        if (
            habit.is_today_due_date or
            habit.today_progress > 0 or
            habit.is_running
        ):
            # 측정 중인 경우 측정 종료
            if habit.is_running:
                record = RoundRecord()
                record.habit = habit
                record.start_datetime: datetime = habit.start_datetime
                record.end_datetime = reset_date
                # TIME 유형인 경우, 현재 시각을 끝으로 진행도 결정
                record.progress = int((record.end_datetime - record.start_datetime).total_seconds())
                record.save()

                habit.start_datetime = None
                habit.is_running = False
                habit.today_progress += record.progress
                habit.due_date = just_a_minute_ago

                user: User = habit.user
                user.is_recording = False                
                user.save()

            # 어제 기록 저장
            daily_record = DailyRecord()
            daily_record.habit = habit
            daily_record.date = yesterday
            daily_record.goal = habit.today_goal
            daily_record.progress = habit.today_progress
            daily_record.success = habit.today_goal <= habit.today_progress
            daily_record.save()
            
            # 오늘 기록 갱신
            if daily_record.success:
                habit.today_goal += habit.growth_amount
            else:
                habit.today_goal -= habit.growth_amount
            habit.today_progress = 0

        # 오늘 해야 하는지
        habit.is_today_due_date = is_due_today_for_habit(habit)
        habit.save()

    # Habit.objects.bulk_update(habit_list, [''])
