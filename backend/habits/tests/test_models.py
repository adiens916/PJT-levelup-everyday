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

    @mock.patch("habits.models_aux.datetime", wraps=datetime)
    def test_is_today_due_date_when_after_due(self, mocked_datetime):
        # when: now is after due date by 1 day
        now = datetime(2022, 9, 4, hour=7, minute=0)
        mocked_datetime.now.return_value = now

        # then: the habit doesn't have to do
        result = DueAdjuster.is_today_due_date(self.habit)
        self.assertFalse(result)

    @mock.patch("habits.models_aux.datetime", wraps=datetime)
    def test_is_today_due_date_when_border_values(self, mocked_datetime):
        # when: now is before due date by 1 minute
        now = datetime(2022, 9, 3, hour=5, minute=59)
        mocked_datetime.now.return_value = now

        # then: the habit doesn't have to do yet
        result = DueAdjuster.is_today_due_date(self.habit)
        self.assertFalse(result)

        # when: now is due
        now = datetime(2022, 9, 3, hour=6, minute=0)
        mocked_datetime.now.return_value = now

        # then: the habit doesn't have to do yet
        result = DueAdjuster.is_today_due_date(self.habit)
        self.assertTrue(result)

        # when: now is before overdue by 1 minute
        now = datetime(2022, 9, 4, hour=5, minute=59)
        mocked_datetime.now.return_value = now

        # then: the habit doesn't have to do yet
        result = DueAdjuster.is_today_due_date(self.habit)
        self.assertTrue(result)
