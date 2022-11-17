from copy import deepcopy

from django.test import TestCase

from habits.models import Habit
from habits.models_aux import GoalAdjuster


class GoalAdjusterTestCase(TestCase):
    def setUp(self) -> None:
        habit = Habit()
        habit.name = "Reading a book"
        habit.growth_type = "INCREASE"
        habit.final_goal = 3600
        habit.today_goal = 60
        habit.today_progress = 0
        habit.growth_amount = 60
        habit.is_today_due_date = True
        self.habit = habit

    def test_habit_copy(self):
        habit_copy = deepcopy(self.habit)
        self.assertNotEqual(id(self.habit), id(habit_copy))

    def test_ignore_for_not_due_habit(self):
        habit_not_due = deepcopy(self.habit)
        habit_not_due.is_today_due_date = False

        GoalAdjuster.adjust_habit_goal(habit_not_due)
        self.assertEqual(habit_not_due.today_goal, 60)

    def test_success_for_increase_type(self):
        pass

    def test_fail_for_increase_type(self):
        pass
