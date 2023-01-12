from datetime import date, datetime, time, timedelta
from unittest import expectedFailure, mock

from django.test import TestCase

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

    def test_create_habit_by_keyword_arguments(self):
        habit_info: HabitCreateType = {"initial_goal": 120}
        new_habit_info = {**HABIT_INFO, **habit_info}
        initial_goal = new_habit_info.get("initial_goal")
        self.assertEqual(initial_goal, 120)

        habit_id = self.provider.create_habit(**habit_info)
        habit_dict = self.__get_habit(habit_id)
        self.assertEqual(habit_dict.get("goal_xp"), 120)

    @mock.patch("account.models_aux.datetime", wraps=datetime)
    def test_lose_xp_for_undone_habit(self, mocked_datetime):
        # [given] habit's goal xp == 300
        habit_id = self.provider.create_habit(initial_goal=300)

        # [when] day changes while habit's undone
        tomorrow = datetime.combine(date.today() + timedelta(days=1), time(0, 0))
        mocked_datetime.now.return_value = tomorrow
        self.__get_habits()

        # [then] habit loses XP for about 10% of goal XP (3600)
        # 3600 * 0.01 == 36 > 30
        habit = self.__get_habit(habit_id)
        self.assertEqual(habit.get("goal_xp"), 270)

        # self.assertEqual(self.habit.goal_xp, 300)
        # current XP should be decreased by 10% of goal XP
        # self.assertEqual(self.habit.current_xp, 120)

    def __get_habits(self) -> None:
        self.client.get("/api/habit/", **self.auth_headers)

    def __get_habit(self, habit_id: int) -> HabitReadType:
        response = self.client.get(f"/api/habit/{habit_id}/", **self.auth_headers)
        data: HabitReadType = response.json()
        return data
