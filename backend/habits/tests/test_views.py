from unittest import mock

from django.test import TestCase, Client

from account.models import User
from habits.models import Habit


class HabitViewTestCase(TestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.user = User.objects.create_user(username="john", password="doe")
        cls.auth_headers = cls.get_auth_headers("john", "doe")
        cls.habit_info = {
            "name": "Reading a book",
            "estimate_type": "TIME",
            "estimate_unit": "",
            "final_goal": 3600,
            "growth_type": "INCREASE",
            "day_cycle": 2,
            "initial_goal": "",
        }

    @classmethod
    def get_auth_headers(cls, username: str, password: str) -> dict:
        credentials = {"username": username, "password": password}
        response = Client().post("/api/account/login/", credentials)

        items: dict = response.json()
        token = items.get("token")
        return {"HTTP_AUTHORIZATION": f"Token {token}"}

    def test_create_habit(self):
        response = self.client.post(
            "/api/habit/", data=self.habit_info, **self.auth_headers
        )

        items: dict = response.json()
        habit_id = items.get("id")
        habit = Habit.objects.get(pk=habit_id)

        self.assertEqual(habit.name, "Reading a book")
        self.assertEqual(habit.final_goal, 3600)
