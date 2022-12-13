from datetime import date, datetime, time, timedelta
from unittest import mock

from django.test import TestCase

from account.models import User
from habits.models import Habit
from habits.models_aux import DueAdjuster


class DueAdjusterTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        """
        Day start: 06:00 AM
        Due date: 2022-09-03
        """

        user = User()
        user.daily_reset_time = time(6, 0)
        user.next_reset_date = date(2022, 9, 4)
        user.save()

        habit = Habit()
        habit.due_date = date(2022, 9, 3)
        habit.is_today_due_date = True
        habit.final_goal = 3600
        habit.day_cycle = 2
        habit.user = user
        habit.save()

        cls.habit = habit

    @mock.patch("habits.models_aux.datetime", wraps=datetime)
    def test_is_today_due_date(self, mocked_datetime):
        now = datetime(2022, 9, 3, hour=7, minute=0)
        mocked_datetime.now.return_value = now

        is_today_due_date = DueAdjuster.is_today_due_date(self.habit)
        self.assertTrue(is_today_due_date)

    @mock.patch("habits.models_aux.datetime", wraps=datetime)
    def test_is_today_due_date_at_exact_time(self, mocked_datetime):
        # when: now is due
        now = datetime(2022, 9, 3, hour=6, minute=0)
        mocked_datetime.now.return_value = now

        # then: the habit doesn't have to do yet
        result = DueAdjuster.is_today_due_date(self.habit)
        self.assertTrue(result)

    @mock.patch("habits.models_aux.datetime", wraps=datetime)
    def test_is_today_due_date_before_day_end(self, mocked_datetime):
        # when: now is before overdue by 1 minute
        now = datetime(2022, 9, 4, hour=5, minute=59)
        mocked_datetime.now.return_value = now

        # then: the habit doesn't have to do yet
        result = DueAdjuster.is_today_due_date(self.habit)
        self.assertTrue(result)

    @mock.patch("habits.models_aux.datetime", wraps=datetime)
    def test_failed_is_today_due_date_before_day_starts(self, mocked_datetime):
        now = datetime(2022, 9, 3, hour=4, minute=0)
        mocked_datetime.now.return_value = now

        is_today_due_date = DueAdjuster.is_today_due_date(self.habit)
        self.assertFalse(is_today_due_date)

    @mock.patch("habits.models_aux.datetime", wraps=datetime)
    def test_failed_is_today_due_date_before_next_due_date(self, mocked_datetime):
        DueAdjuster.adjust_habit_due(self.habit)

        # when: now is after due date by 1 day
        now = datetime(2022, 9, 4, hour=7, minute=0)
        mocked_datetime.now.return_value = now

        # then: the habit doesn't have to do
        is_today_due_date = DueAdjuster.is_today_due_date(self.habit)
        self.assertFalse(is_today_due_date)

    @mock.patch("habits.models_aux.datetime", wraps=datetime)
    def test_is_today_due_date_on_next_day_cycle(self, mocked_datetime):
        DueAdjuster.adjust_habit_due(self.habit)

        now = datetime(2022, 9, 5, hour=7, minute=0)
        mocked_datetime.now.return_value = now

        result = DueAdjuster.is_today_due_date(self.habit)
        self.assertTrue(result)
