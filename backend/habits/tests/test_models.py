from datetime import date, datetime, time, timedelta
from unittest import mock

from django.test import TestCase

from account.models import User
from habits.models import Habit
from habits.models_aux import DueAdjuster


class HabitModelTestCase(TestCase):
    def setUp(self) -> None:
        self.habit = Habit()
        self.habit.user = User()

        # given: the habit is to do at 2022-09-03
        self.habit.due_date = date(2022, 9, 3)
        user: User = self.habit.user
        # given: the owner of the habit starts the day at AM 06:00
        user.daily_reset_time = time(6, 0)
        user.save()

    @mock.patch("habits.models_aux.datetime", wraps=datetime)
    def test_is_today_due_date(self, mocked_datetime):
        # when: now is 2022-09-03 AM 07:00
        now = datetime(2022, 9, 3, hour=7, minute=0)
        mocked_datetime.now.return_value = now

        # then: the habit is to do today
        result = DueAdjuster.is_today_due_date(self.habit)
        self.assertIs(result, True)

    # def test_is_today_due_date_when_border_values():
    #     due_date = date(2022, 9, 1)
    #     reset_hour = time(6, 0)

    #     day_cycle = 2
    #     next_due_date = due_date + timedelta(days=day_cycle)

    #     now = datetime(2022, 9, 3, hour=5, minute=59)
    #     assert False == is_due_today(next_due_date, reset_hour, now)

    #     now = datetime(2022, 9, 4, hour=5, minute=59)
    #     assert True == is_due_today(next_due_date, reset_hour, now)

    # def test_is_today_due_date_when_after_due():
    #     due_date = date(2022, 9, 1)
    #     reset_hour = time(6, 0)

    #     day_cycle = 2
    #     next_due_date = due_date + timedelta(days=day_cycle)

    #     now = datetime(2022, 9, 7, hour=6, minute=0)
    #     assert False == is_due_today(next_due_date, reset_hour, now)
