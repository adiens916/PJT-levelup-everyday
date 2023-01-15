from datetime import date, time, timedelta
from unittest import expectedFailure
from django.test import TestCase

from habits.models import Habit
from .provider import TestDataProvider


class HabitViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        provider = TestDataProvider()

        cls.auth_headers = provider.get_auth_headers()
        provider.user.last_reset_date = date.today() + timedelta(days=1)
        provider.user.reset_time = time(0, 0)
        provider.user.save()

        cls.habit_id = provider.create_habit()
        provider.create_habits()

    def test_create_habit(self):
        habit = Habit.objects.get(pk=self.habit_id)
        self.assertEqual(habit.name, "Reading a book")
        self.assertEqual(habit.final_goal, 3600)
        self.assertEqual(habit.goal_xp, 300)

    def test_get_habits(self):
        response = self.client.get("/api/habit/", **self.auth_headers)
        data: list[dict] = response.json()

        self.assertIsInstance(data, list)
        self.assertIsInstance(data[0], dict)
        self.assertEqual(len(data), 3)

        self.assertContains(response, "current_xp")

    def test_get_a_habit(self):
        response = self.client.get(f"/api/habit/{self.habit_id}/", **self.auth_headers)
        data: dict = response.json()

        self.assertIsInstance(data, dict)

    def test_delete_habit(self):
        pass

    def test_update_importance(self):
        pass
