import json
from datetime import datetime, time, timedelta
from typing import Iterable

from django.core import serializers
from django.db.models import Model
from django.http import JsonResponse

from account.models import User
from .models import Habit


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
    delta = timedelta(day_cycle)
    return date_done_last + delta <= now
