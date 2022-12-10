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

    def test_adjust_habit_goal_not_due(self):
        self.habit.is_today_due_date = False
        GoalAdjuster.adjust_habit_goal(self.habit)
        self.assertEqual(self.habit.goal_xp, 60)
        self.assertEqual(self.habit.current_xp, 0)

    def test_adjust_habit_goal(self):
        self.habit.current_xp = 60
        GoalAdjuster.adjust_habit_goal(self.habit)
        self.assertEqual(self.habit.goal_xp, 120)
        self.assertEqual(self.habit.current_xp, 0)

    def test_adjust_habit_goal_done_just_a_little(self):
        self.habit.current_xp = 5

        GoalAdjuster.adjust_habit_goal(self.habit)
        self.assertEqual(self.habit.goal_xp, 60)
        self.assertEqual(self.habit.current_xp, 5)

    def test_adjust_habit_goal_neglected(self):
        self.habit.goal_xp = 300
        self.habit.current_xp = 150

        GoalAdjuster.adjust_habit_goal(self.habit)
        self.assertEqual(self.habit.goal_xp, 300)
        # current XP should be decreased by 10% of goal XP
        self.assertEqual(self.habit.current_xp, 120)

    def test_adjust_habit_goal_neglected_with_level_down(self):
        """
        When the current XP is 0, then it can't be decreased below zero.
        Therefore, the goal XP will be decreased instead,
        followed by decrease of current XP.

        The amount of decrease is based on the **new** goal XP.
        If not so, a current XP could be greater than the goal XP.
        """

        self.habit.goal_xp = 300
        self.habit.current_xp = 0

        GoalAdjuster.adjust_habit_goal(self.habit)
        self.assertEqual(self.habit.goal_xp, 240)
        self.assertEqual(self.habit.current_xp, 216)

    def test_adjust_habit_goal_neglected_without_level_down(self):
        self.habit.goal_xp = 60
        self.habit.current_xp = 0

        GoalAdjuster.adjust_habit_goal(self.habit)
        self.assertEqual(self.habit.goal_xp, 60)
        self.assertEqual(self.habit.current_xp, 0)
