from datetime import date, datetime, time

from django.test import TestCase

from account.models import User
from habits.models import Habit, RoundRecord, DailyRecord
from habits.models_aux import RecordSaver


class RecordSaverTestCase(TestCase):
    def setUp(self) -> None:
        habit = Habit()
        habit.name = "Reading a book"
        habit.estimate_type = "TIME"
        habit.growth_type = "INCREASE"
        habit.final_goal = 3600
        habit.goal_xp = 60
        habit.current_xp = 70
        habit.growth_amount = 60
        habit.is_today_due_date = True
        self.habit = habit

        user = User()
        user.next_reset_date = date(2022, 11, 11)
        user.daily_reset_time = time(hour=0, minute=0)
        user.save()
        self.habit.user = user
        self.habit.save()

    def test_create_round_record(self):
        self.habit.is_running = True
        self.habit.start_datetime = datetime(2022, 11, 10, hour=23, minute=50)
        self.habit.save()

        RecordSaver.save(self.habit)
        round_record = RoundRecord.objects.get(habit=self.habit)
        self.assertEqual(
            round_record.start_datetime, datetime(2022, 11, 10, hour=23, minute=50)
        )
        self.assertEqual(
            round_record.end_datetime, datetime(2022, 11, 10, hour=23, minute=59)
        )
        self.assertEqual(round_record.progress, 60 * 9)

    def test_create_daily_record(self):
        RecordSaver.save(self.habit)
        daily_record = DailyRecord.objects.get(habit=self.habit)
        self.assertEqual(daily_record.date, date(2022, 11, 10))
        self.assertEqual(daily_record.success, True)
        self.assertEqual(daily_record.goal, 60)
        self.assertEqual(daily_record.progress, 60)
        self.assertEqual(daily_record.excess, 70)

    def test_create_records_if_habit_is_done_but_not_due(self):
        self.habit.is_today_due_date = False
        self.habit.save()

        RecordSaver.save(self.habit)
        daily_record = DailyRecord.objects.get(habit=self.habit)
        self.assertEqual(daily_record.success, True)
        self.assertEqual(daily_record.goal, 60)
        self.assertEqual(daily_record.progress, 60)
        self.assertEqual(daily_record.excess, 70)

    def test_create_records_if_habit_is_not_completed(self):
        self.habit.current_xp = 10
        self.habit.save()

        RecordSaver.save(self.habit)
        daily_record = DailyRecord.objects.get(habit=self.habit)
        self.assertEqual(daily_record.date, date(2022, 11, 10))
        self.assertEqual(daily_record.success, False)
        self.assertEqual(daily_record.goal, 60)
        self.assertEqual(daily_record.progress, 10)
        self.assertEqual(daily_record.excess, 0)
