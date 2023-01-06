from datetime import date, time, timedelta
from unittest import expectedFailure
from django.test import TestCase

from habits.models import Habit, DailyRecord
from habits.models_type import DailyRecordType
from .provider import TestDataProvider


class HabitViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        provider = TestDataProvider()

        cls.auth_headers = provider.get_auth_headers()
        provider.user.next_reset_date = date.today() + timedelta(days=1)
        provider.user.daily_reset_time = time(0, 0)
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

    def test_daily_record_created_at_first(self):
        response = self.client.get(
            f"/api/habit/{self.habit_id}/record/", **self.auth_headers
        )
        data: list[DailyRecordType] = response.json()

        self.assertEqual(len(data), 1)

        first_record = data[0]
        self.assertEqual(first_record.get("habit"), self.habit_id)
        self.assertEqual(first_record.get("date"), date.today().isoformat())
        self.assertEqual(first_record.get("level_now"), 1)
        self.assertEqual(first_record.get("level_change"), 0)
        self.assertEqual(first_record.get("xp_now"), 0)
        self.assertEqual(first_record.get("xp_change"), 0)

    def test_daily_record_updated_when_round_finished(self):
        self.__record_habit_progress(60)
        record = self.__get_record_by_request()
        self.assertEqual(record.get("xp_now"), 60)
        self.assertEqual(record.get("xp_change"), 60)

    def __record_habit_progress(self, progress: int) -> None:
        self.client.post(
            f"/api/habit/timer/start/", {"habit_id": self.habit_id}, **self.auth_headers
        )
        self.client.post(
            f"/api/habit/timer/finish/",
            {"habit_id": self.habit_id, "progress": progress},
            **self.auth_headers,
        )

    def __get_record_by_request(self) -> DailyRecordType:
        response = self.client.get(
            f"/api/habit/{self.habit_id}/record/", **self.auth_headers
        )
        data: list[DailyRecordType] = response.json()
        record = data[0]
        return record

    @expectedFailure
    def test_get_daily_records(self):
        response = self.client.get(
            f"/api/habit/{self.habit_id}/record/", **self.auth_headers
        )
        data: dict = response.json()

        self.assertContains(response, "date")
        self.assertContains(response, "success")
        self.assertContains(response, "level_now")
        self.assertContains(response, "level_change")
        self.assertContains(response, "xp_now")
        self.assertContains(response, "xp_change")
