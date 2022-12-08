from datetime import datetime, timedelta
from unittest import mock

from django.test import TestCase, Client

from account.models import User
from habits.models import Habit, RoundRecord


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
            "initial_goal": 300,
        }
        cls.habit_id = cls.create_habit()

    @classmethod
    def get_auth_headers(cls, username: str, password: str) -> dict:
        credentials = {"username": username, "password": password}
        response = Client().post("/api/account/login/", credentials)

        items: dict = response.json()
        token = items.get("token")
        return {"HTTP_AUTHORIZATION": f"Token {token}"}

    @classmethod
    def create_habit(cls) -> int:
        response = Client().post("/api/habit/", data=cls.habit_info, **cls.auth_headers)

        items: dict = response.json()
        habit_id = items.get("id")
        return habit_id

    def test_create_habit(self):
        habit = Habit.objects.get(pk=self.habit_id)
        self.assertEqual(habit.name, "Reading a book")
        self.assertEqual(habit.final_goal, 3600)
        self.assertEqual(habit.goal_xp, 300)

    def test_start_timer(self):
        before = datetime.now()
        self.client.post(
            "/api/habit/timer/start/", {"habit_id": self.habit_id}, **self.auth_headers
        )
        after = datetime.now()

        habit = Habit.objects.get(pk=self.habit_id)
        self.assertTrue(habit.is_running)

        self.assertIsInstance(habit.start_datetime, datetime)
        self.assertGreaterEqual(habit.start_datetime, before - timedelta(minutes=1))
        self.assertLessEqual(habit.start_datetime, after + timedelta(minutes=1))

    def test_finish_timer(self):
        self.test_start_timer()

        habit = Habit.objects.get(pk=self.habit_id)
        self.assertTrue(habit.is_running)

        self.client.post(
            "/api/habit/timer/finish/",
            {"habit_id": self.habit_id, "progress": 45},
            **self.auth_headers,
        )

        round_record = RoundRecord.objects.get(habit=habit)
        self.assertEqual(round_record.progress, 45)

        habit = Habit.objects.get(pk=self.habit_id)
        self.assertEqual(habit.goal_xp, 300)
        self.assertEqual(habit.current_xp, 45)
