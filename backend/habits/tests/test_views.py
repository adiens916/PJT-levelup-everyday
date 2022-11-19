from unittest import mock

from django.test import TestCase

from account.models import User
from habits.models import Habit


class HabitViewTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="john", password="doe")
        self.habit_info = {
            "name": "Reading a book",
            "estimate_type": "TIME",
            "estimate_unit": "",
            "final_goal": 3600,
            "growth_type": "INCREASE",
            "day_cycle": 2,
            "initial_goal": "",
        }

    def test_create_habit(self):
        self.assertFalse(Habit.objects.exists())

        credentials = {"username": "john", "password": "doe"}
        response = self.client.post("/api/account/login/", credentials)

        items: dict = response.json()
        token = items.get("token")
        headers = {"HTTP_AUTHORIZATION": f"Token {token}"}

        response = self.client.post("/api/habit/", data=self.habit_info, **headers)
        # print(response.content)

        items: dict = response.json()
        habit_id = items.get("id")
        # print(habit_id)

        habit = Habit.objects.get(pk=habit_id)
        self.assertEqual(habit.name, "Reading a book")
        self.assertEqual(habit.final_goal, 3600)
