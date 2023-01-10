from datetime import date, datetime, time

from django.test import TestCase

from account.models import User
from habits.models import Habit, RoundRecord, DailyRecord
from habits.models_aux import RecordSaver


class RecordSaverTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User()
        user.next_reset_date = date(2022, 11, 11)
        user.daily_reset_time = time(hour=0, minute=0)
        user.save()

        habit = Habit()
        habit.name = "Reading a book"
        habit.estimate_type = "TIME"
        habit.growth_type = "INCREASE"
        habit.final_goal = 3600
        habit.level = 1
        habit.goal_xp = 60
        habit.current_xp = 50
        habit.growth_amount = 60
        habit.is_today_due_date = True
        habit.is_done = True

        cls.habit = habit
        cls.habit.user = user
        cls.habit.save()
