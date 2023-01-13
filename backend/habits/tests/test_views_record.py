from datetime import date, datetime, time, timedelta
from unittest import expectedFailure, mock
from django.test import TestCase

from habits.models_type import DailyRecordType
from .provider import TestDataProvider


class HabitViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        provider = TestDataProvider()

        cls.auth_headers = provider.get_auth_headers()
        provider.user.last_reset_date = date.today()
        provider.user.reset_time = time(0, 0)
        provider.user.save()

        cls.habit_id = provider.create_habit()
        provider.create_habits()

    def test_daily_record_created_at_first(self):
        records = self.__get_records()
        self.assertEqual(len(records), 1)

        first_record = records[0]
        self.assertEqual(first_record.get("habit"), self.habit_id)
        self.assertEqual(first_record.get("date"), date.today().isoformat())
        self.assertEqual(first_record.get("level_now"), 1)
        self.assertEqual(first_record.get("level_change"), 0)
        self.assertEqual(first_record.get("xp_now"), 0)
        self.assertEqual(first_record.get("xp_change"), 0)

    @mock.patch("account.models_aux.datetime", wraps=datetime)
    def test_daily_record_created_after_days_passed(self, mocked_datetime):
        # [given] assuming a daily record has existed already
        records = self.__get_records()
        self.assertEqual(len(records), 1)

        # [given] 3 days has passed after a user visited
        now = datetime.today() + timedelta(days=3)
        mocked_datetime.now.return_value = now

        # [when] the user logs in and get habit list
        self.client.get("/api/habit/", **self.auth_headers)

        # [then] the new daily record for today should exist
        records = self.__get_records()
        self.assertEqual(len(records), 2)

        latest_record = records[1]
        self.assertEqual(latest_record.get("date"), now.date().isoformat())
        self.assertEqual(latest_record.get("xp_change"), 0)

    def test_daily_record_updated_when_round_finished(self):
        self.__record_habit_progress(60)
        record = self.__get_record_by_request()
        self.assertEqual(record.get("xp_now"), 60)
        self.assertEqual(record.get("xp_change"), 60)

    def test_daily_record_updated_when_round_finished_continuously(self):
        # [given]
        # habit's initial goal == 300
        # habit's growth amount == 30
        response = self.client.get(f"/api/habit/{self.habit_id}/", **self.auth_headers)
        data: dict = response.json()
        self.assertEqual(data.get("goal_xp"), 300)
        self.assertEqual(data.get("growth_amount"), 30)

        # [given] it has record for 60 seconds
        try:
            record = self.__get_record_by_request()
            self.assertEqual(record.get("xp_now"), 60)
            self.assertEqual(record.get("xp_change"), 60)
        except:
            self.__record_habit_progress(60)

        # [when] adding 200 seconds
        self.__record_habit_progress(200)
        record = self.__get_record_by_request()
        # [then] total 260 seconds
        self.assertEqual(record.get("xp_now"), 260)
        self.assertEqual(record.get("xp_change"), 260)

        # [when] adding 150 seconds
        self.__record_habit_progress(150)
        record = self.__get_record_by_request()
        # [then] level increased & xp subtracted
        self.assertEqual(record.get("level_now"), 2)
        self.assertEqual(record.get("level_change"), 1)
        self.assertEqual(record.get("xp_now"), 110)
        self.assertEqual(record.get("xp_change"), 410)

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

    def __get_records(self) -> list[DailyRecordType]:
        response = self.client.get(
            f"/api/habit/{self.habit_id}/record/", **self.auth_headers
        )
        data: list[DailyRecordType] = response.json()
        return data

    def __record_habit_progress(self, progress: int) -> None:
        self.client.post(
            f"/api/habit/timer/start/", {"habit_id": self.habit_id}, **self.auth_headers
        )
        self.client.post(
            f"/api/habit/timer/finish/",
            {"habit_id": self.habit_id, "progress": progress},
            **self.auth_headers,
        )

    def __get_record_by_request(self, index=0) -> DailyRecordType:
        response = self.client.get(
            f"/api/habit/{self.habit_id}/record/", **self.auth_headers
        )
        data: list[DailyRecordType] = response.json()
        record = data[index]
        return record
