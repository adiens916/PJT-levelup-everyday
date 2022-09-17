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


def is_due_today(due_date: date, reset_hour: time, now: datetime):
    if due_date == None:
        return False

    due_date_start = datetime.combine(due_date, reset_hour)
    due_date_end = due_date_start + timedelta(days=1)

    if now < due_date_start:
        return False
    elif due_date_start <= now < due_date_end:
        return True
    elif due_date_end <= now:
        # 원래 예정일에 접속했더라면 알아서 다음 날로 갱신이 됨.
        # 이 경우는 예정일에 아예 접속조차 안 해서 갱신이 안 됐던 상황.
        # 밀린 게 쌓였을 수 있으므로, 부담을 줄이기 위해 예정에서 빼놓기
        return False


def test_is_due_today():
    due_date = date(2022, 9, 1)
    reset_hour = time(6, 0)

    day_cycle = 2
    next_due_date = due_date + timedelta(days=day_cycle)

    now = datetime(2022, 9, 3, hour=6, minute=0)
    assert True == is_due_today(next_due_date, reset_hour,  now)


def test_is_due_today_when_border_values():
    due_date = date(2022, 9, 1)
    reset_hour = time(6, 0)
    
    day_cycle = 2
    next_due_date = due_date + timedelta(days=day_cycle)

    now = datetime(2022, 9, 3, hour=5, minute=59)
    assert False == is_due_today(next_due_date, reset_hour, now)

    now = datetime(2022, 9, 4, hour=5, minute=59)
    assert True == is_due_today(next_due_date, reset_hour, now)


def test_is_due_today_when_after_due():
    due_date = date(2022, 9, 1)
    reset_hour = time(6, 0)

    day_cycle = 2
    next_due_date = due_date + timedelta(days=day_cycle)

    now = datetime(2022, 9, 7, hour=6, minute=0)
    assert False == is_due_today(next_due_date, reset_hour,  now)
