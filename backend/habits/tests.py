from datetime import datetime, timedelta
from django.test import TestCase

# Create your tests here.
def is_due_today(date_done_last: datetime, day_cycle: int, now: datetime):
    delta = timedelta(day_cycle)
    return date_done_last + delta <= now


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
