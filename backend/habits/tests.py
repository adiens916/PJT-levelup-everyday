'''
모델 관련한 테스트는 Django 설정이 필요하므로 pytest로 검사하면 오류 남.
=> 테스트 대상이 되는 함수를 이쪽으로 옮겨옴.
'''

from datetime import datetime, time, timedelta
from django.test import TestCase


# Create your tests here.
def is_day_changed(date_reset_last: datetime, reset_time: time, now: datetime):
    if not date_reset_last:
        return True

    # 최근 갱신 시간이 초기화 시간을 넘은 경우, 이미 지났을 거라고 판단
    if date_reset_last.time() > reset_time:
        # 다음 날은 하루 뒤여야 함.
        tomorrow = date_reset_last + timedelta(days=1) 
    else:
        # 초기화 시간을 안 넘은 경우, 초기화는 같은 날에 일어남.
        tomorrow = date_reset_last

    date_when_reset = datetime.combine(tomorrow.date(), reset_time)
    return now >= date_when_reset


def test_is_day_changed_for_morning():
    yesterday_morning = datetime(2022, 9, 1, hour=9)
    at_dawn = time(5, 30)

    today_midnight = datetime(2022, 9, 2, hour=0)
    assert False == is_day_changed(yesterday_morning, at_dawn, today_midnight)

    today_dawn = datetime(2022, 9, 2, hour=6)
    assert True == is_day_changed(yesterday_morning, at_dawn, today_dawn)


def test_is_day_changed_for_night():
    yesterday_morning = datetime(2022, 9, 1, hour=22)
    at_dawn = time(1, 30)

    today_midnight = datetime(2022, 9, 2, hour=0)
    assert False == is_day_changed(yesterday_morning, at_dawn, today_midnight)

    today_dawn = datetime(2022, 9, 2, hour=2)
    assert True == is_day_changed(yesterday_morning, at_dawn, today_dawn)


def test_is_day_changed_for_same_day():
    today_night = datetime(2022, 9, 1, hour=22, minute=0)
    at_night = time(hour=22, minute=15)
    today_night_after_minutes = datetime(2022, 9, 1, hour=22, minute=30)
    assert True == is_day_changed(today_night, at_night, today_night_after_minutes)


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
