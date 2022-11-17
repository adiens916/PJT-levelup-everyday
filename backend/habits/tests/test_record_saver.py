from copy import deepcopy

from django.test import TestCase

from habits.models import Habit, RoundRecord, DailyRecord
from habits.models_aux import RecordSaver


class RecordSaverTestCase(TestCase):
    def setUp(self) -> None:
        habit = Habit()
        habit.name = "Reading a book"
        habit.growth_type = "INCREASE"
        habit.final_goal = 3600
        habit.today_goal = 60
        habit.today_progress = 70
        habit.growth_amount = 60
        habit.is_today_due_date = True
        self.habit = habit

    def test_ensure_no_records_before_save(self):
        self.assertFalse(RoundRecord.objects.exists())
        self.assertFalse(DailyRecord.objects.exists())
