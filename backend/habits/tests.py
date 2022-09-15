from datetime import datetime, timedelta
from django.test import TestCase

# Create your tests here.
def is_day_changed(last_done_date: datetime, day_cycle: int, now: datetime):
    delta = timedelta(day_cycle)
    return last_done_date + delta <= now


def test_is_day_changed():
    last_done_date = datetime(2022, 9, 1, 9)
    day_cycle = 1

    not_yet_tomorrow = datetime(year=2022, month=9, day=2, hour=8, minute=59)
    assert False == is_day_changed(last_done_date, day_cycle, not_yet_tomorrow)

    tomorrow = datetime(year=2022, month=9, day=2, hour=9)
    assert True == is_day_changed(last_done_date, day_cycle, tomorrow)

    day_cycle = 3
    after_a_number_of_days = datetime(year=2022, month=9, day=7, hour=9)
    assert True == is_day_changed(last_done_date, day_cycle, after_a_number_of_days)
