from datetime import date, time, timedelta
from unittest import expectedFailure

from django.test import TestCase

from habits.models import Habit
from habits.models_type import HabitCreateType, HabitReadType
from .provider import TestDataProvider, HABIT_INFO


class HabitViewDayChangeTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.provider = TestDataProvider()

        cls.auth_headers = cls.provider.get_auth_headers()
        cls.provider.user.last_reset_date = date.today()
        cls.provider.user.reset_time = time(0, 0)
        cls.provider.user.save()

    # def setUp(self) -> None:
    #     self.habit_id = self.provider.create_habit()

    def test_create_habit_by_keyword_arguments(self):
        habit_info: HabitCreateType = {"initial_goal": 120}
        new_habit_info = {**HABIT_INFO, **habit_info}
        initial_goal = new_habit_info.get("initial_goal")
        self.assertEqual(initial_goal, 120)

        habit_id = self.provider.create_habit(**habit_info)
        habit_dict = self.__get_habit(habit_id)
        self.assertEqual(habit_dict.get("goal_xp"), 120)

    # def test_adjust_habit_goal_neglected(self):
    #     self.habit.goal_xp = 300
    #     self.habit.current_xp = 150

    #     self.habit.end_recording(5, False)
    #     GoalAdjuster.adjust_habit_goal(self.habit)
    #     self.assertEqual(self.habit.goal_xp, 300)
    #     # current XP should be decreased by 10% of goal XP
    #     self.assertEqual(self.habit.current_xp, 120)

    def __get_habits(self) -> None:
        self.client.get("/api/habit/", **self.auth_headers)

    def __get_habit(self, habit_id: int) -> HabitReadType:
        response = self.client.get(f"/api/habit/{habit_id}/", **self.auth_headers)
        data: HabitReadType = response.json()
        return data
