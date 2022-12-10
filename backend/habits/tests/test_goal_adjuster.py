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
        habit.goal_xp = 60
        habit.current_xp = 0
        habit.growth_amount = 60
        habit.is_today_due_date = True
        self.habit = habit

    def test_adjust_habit_goal_when_not_due(self):
        self.habit.is_today_due_date = False
        GoalAdjuster.adjust_habit_goal(self.habit)
        self.assertEqual(self.habit.goal_xp, 60)

    def test_adjust_habit_goal(self):
        self.habit.current_xp = 60
        GoalAdjuster.adjust_habit_goal(self.habit)
        self.assertEqual(self.habit.goal_xp, 120)
        self.assertEqual(self.habit.current_xp, 0)

    def test_adjust_habit_goal_when_not_reaching_goal(self):
        self.habit.current_xp = 10
        GoalAdjuster.adjust_habit_goal(self.habit)
        # TODO: prevent today_goal from decreasing below 0
        # self.assertEqual(self.habit.today_goal, 60)
        self.assertEqual(self.habit.current_xp, 0)
