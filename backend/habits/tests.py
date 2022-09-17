'''
모델 관련한 테스트는 Django 설정이 필요하므로 pytest로 검사하면 오류 남.
=> 테스트 대상이 되는 함수를 이쪽으로 옮겨옴.
'''

from datetime import datetime, time, timedelta, date
from django.test import TestCase


# Create your tests here.
def is_day_changed(next_reset_date: date, daily_reset_time: time, now: datetime):
    if next_reset_date == None:
        return True

    next_reset_datetime = datetime.combine(next_reset_date, daily_reset_time)
    return next_reset_datetime <= now


def test_is_day_changed_when_reset_at_night():
    reset_date = date(2022, 9, 1)
    reset_hour = time(22, 15)
    now = datetime(2022, 9, 1, hour=22, minute=30)
    assert True == is_day_changed(reset_date, reset_hour, now)


def test_is_day_changed_when_reset_at_dawn():
    reset_date = date(2022, 9, 17)
    reset_hour = time(6, 0)

    now = datetime(2022, 9, 17, hour=0)
    assert False == is_day_changed(reset_date, reset_hour, now)

    now = datetime(2022, 9, 17, hour=7)
    assert True == is_day_changed(reset_date, reset_hour, now)


def is_due_today(date_done_last: datetime, day_cycle: int, now: datetime):
    if date_done_last == None:
        return False

    # FIXME: 초기화 시간 고려해서 해야 함
    days = timedelta(day_cycle)
    return date_done_last + days <= now


def test_is_due_today():
    date_done_last = datetime(2022, 9, 1, 9)
    day_cycle = 1

    not_yet_tomorrow = datetime(year=2022, month=9, day=2, hour=8, minute=59)
    assert False == is_due_today(date_done_last, day_cycle, not_yet_tomorrow)

    tomorrow = datetime(year=2022, month=9, day=2, hour=9)
    assert True == is_due_today(date_done_last, day_cycle, tomorrow)


def test_is_due_today_for_long_term():
    date_done_last = datetime(2022, 9, 1, 9)
    day_cycle = 3

    date_after_six_days = datetime(year=2022, month=9, day=7, hour=9)
    assert True == is_due_today(date_done_last, day_cycle, date_after_six_days)
