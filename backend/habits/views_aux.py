import json
from datetime import datetime, time, timedelta
from typing import Iterable

from django.core import serializers
from django.db.models import Model
from django.http import JsonResponse

from account.models import User
from .models import DailyRecord, Habit, RoundRecord


def json_response_wrapper(queryset: Iterable[Model]):
    queryset_json = serializers.serialize('json', queryset, ensure_ascii=False)
    queryset_dict = json.loads(queryset_json)
    return JsonResponse(queryset_dict, safe=False)


def is_day_changed(date_reset_last: datetime, reset_time: time, now: datetime):
    if not date_reset_last:
        return True

    tomorrow = date_reset_last + timedelta(days=1) 
    date_when_reset = datetime.combine(tomorrow.date(), reset_time)
    return now >= date_when_reset


def is_day_changed_for_user(user: User):
    return is_day_changed(
        user.last_reset_date, 
        user.standard_reset_time, 
        datetime.now()
    )


def is_due_today(date_done_last: datetime, day_cycle: int, now: datetime):
    # FIXME: 초기화 시간 고려해서 해야 함
    days = timedelta(day_cycle)
    return date_done_last + days <= now


def is_due_today_for_habit(habit: Habit):
    return is_due_today(
        habit.last_done_date, 
        habit.day_cycle, 
        datetime.now()
    )


def update_goals_and_due_dates(habit_list: Iterable[Habit]):
    '''
    오늘이 예정일인 경우,
    이전의 성공/실패 여부를 참고해
    오늘 목표를 조정한다.
    '''

    reset_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    just_a_minute_ago = reset_date - timedelta(minutes=1)
    yesterday = reset_date - timedelta(days=1)

    for habit in habit_list:
        if (
            habit.is_due_today or
            habit.today_progress > 0 or
            habit.is_running
        ):
            # 측정 중인 경우 측정 종료
            if habit.is_running:
                record = RoundRecord()
                record.habit = habit
                record.start_date: datetime = habit.start_date
                record.end_date = reset_date
                # TIME 유형인 경우, 현재 시각을 끝으로 진행도 결정
                record.progress = int((record.end_date - record.start_date).total_seconds())
                record.save()

                habit.start_date = None
                habit.is_running = False
                habit.today_progress += record.progress
                habit.last_done_date = just_a_minute_ago

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
        habit.is_due_today = is_due_today_for_habit(habit)
        habit.save()

    # Habit.objects.bulk_update(habit_list, [''])
