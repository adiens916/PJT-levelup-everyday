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
        habit.current_xp = 70
        habit.growth_amount = 60
        habit.is_today_due_date = True
        habit.is_done = True

        cls.habit = habit
        cls.habit.user = user
        cls.habit.save()

    def test_create_round_record_if_running(self):
        CLOSE_TO_RESET = datetime(2022, 11, 10, hour=23, minute=50)
        SHORTLY_BEFORE_RESET = datetime(2022, 11, 10, hour=23, minute=59)

        self.habit.is_running = True
        self.habit.start_datetime = CLOSE_TO_RESET
        self.habit.save()

        RecordSaver.save(self.habit)
        round_record = RoundRecord.objects.get(habit=self.habit)
        self.assertEqual(round_record.start_datetime, CLOSE_TO_RESET)
        self.assertEqual(round_record.end_datetime, SHORTLY_BEFORE_RESET)
        self.assertEqual(round_record.progress, 60 * 9)

    def test_create_daily_record(self):
        RecordSaver.save(self.habit)
        daily_record = DailyRecord.objects.get(habit=self.habit)
        self.assertEqual(daily_record.date, date(2022, 11, 10))
        self.assertEqual(daily_record.success, True)
        self.assertEqual(daily_record.level_now, 2)
        self.assertEqual(daily_record.level_change, 1)
        self.assertEqual(daily_record.xp_now, 10)
        self.assertEqual(daily_record.xp_change, 70)

    def test_create_records_if_habit_is_done_but_not_due(self):
        self.habit.is_today_due_date = False
        self.habit.save()

        RecordSaver.save(self.habit)
        daily_record = DailyRecord.objects.get(habit=self.habit)
        self.assertEqual(daily_record.success, True)
        self.assertEqual(daily_record.level_now, 2)
        self.assertEqual(daily_record.level_change, 1)
        self.assertEqual(daily_record.xp_now, 10)
        self.assertEqual(daily_record.xp_change, 70)

    def test_create_records_if_habit_is_not_completed(self):
        self.habit.current_xp = 10
        self.habit.save()

        RecordSaver.save(self.habit)
        daily_record = DailyRecord.objects.get(habit=self.habit)
        self.assertEqual(daily_record.date, date(2022, 11, 10))
        self.assertEqual(daily_record.success, True)
        self.assertEqual(daily_record.level_now, 1)
        self.assertEqual(daily_record.level_change, 0)
        self.assertEqual(daily_record.xp_now, 10)
        self.assertEqual(daily_record.xp_change, 10)
