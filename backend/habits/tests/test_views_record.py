from datetime import date, datetime, time, timedelta
from unittest import expectedFailure, mock
from django.test import TestCase

from habits.models import Habit, RoundRecord, DailyRecord
from habits.models_type import DailyRecordType, HabitReadType
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

    def tearDown(self) -> None:
        # [setup] delete previous records
        DailyRecord.objects.filter(habit=self.habit_id).all().delete()
        RoundRecord.objects.filter(habit=self.habit_id).all().delete()

        # [setup] initialize habit
        habit = Habit.objects.get(pk=self.habit_id)
        habit.level = 1
        habit.day_cycle = 2
        habit.goal_xp = 300
        habit.current_xp = 0
        habit.save()

        # [setup] make an initial daily record
        DailyRecord.create_or_update_from_habit(habit)

        return super().tearDown()

    def test_daily_record_created_at_first(self):
        records = self.__get_records()
        self.assertEqual(len(records), 1)

        first_record = records[0]
        self.assertEqual(first_record.get("habit"), self.habit_id)
        self.assertEqual(first_record.get("date"), date.today().isoformat())
        self.assertEqual(first_record.get("level_now"), 1)
        self.assertEqual(first_record.get("level_change"), 0)
        self.assertEqual(first_record.get("xp_accumulate"), 0)
        self.assertEqual(first_record.get("xp_change"), 0)

    @mock.patch("account.models_aux.datetime", wraps=datetime)
    def test_daily_record_created_after_days_passed(self, mocked_datetime):
        # [given] assuming a daily record has existed already
        records = self.__get_records()
        self.assertEqual(len(records), 1)

        # [given] 3 days has passed after a user visited
        after_three_days = datetime.today() + timedelta(days=3)
        mocked_datetime.now.return_value = after_three_days

        # [when] the user logs in and get habit list
        self.__get_habits()

        # [then] the new daily record for today should exist
        records = self.__get_records()
        self.assertEqual(len(records), 2)

        latest_record = records[1]
        self.assertEqual(latest_record.get("date"), after_three_days.date().isoformat())
        self.assertEqual(latest_record.get("xp_change"), 0)

    @mock.patch("account.models_aux.datetime", wraps=datetime)
    def test_daily_record_created_for_habit_not_due(self, mocked_datetime):
        # [given] day cycle == 2
        habit = self.__get_habit()
        self.assertEqual(habit.get("day_cycle"), 2)

        # [when] on the next day
        tomorrow = datetime.today() + timedelta(days=1)
        mocked_datetime.now.return_value = tomorrow
        self.__get_habits()

        # [then] it doesn't make a new daily record
        records = self.__get_records()
        self.assertEqual(len(records), 1)

        # [when] the user has started recording
        self.__record_habit_progress(60)

        # [then] a new daily record has been created
        records = self.__get_records()
        self.assertEqual(len(records), 2)

        today_record = records[1]
        self.assertEqual(today_record.get("xp_change"), 60)

    @mock.patch("account.models_aux.datetime", wraps=datetime)
    def test_daily_record_level_change(self, mocked_datetime):
        # [given] on the first day, level change == 0
        record = self.__get_first_record()
        self.assertEqual(record.get("level_now"), 1)
        self.assertEqual(record.get("level_change"), 0)

        # [when] on the next day, record progress by 300
        tomorrow = datetime.today() + timedelta(days=1)
        mocked_datetime.now.return_value = tomorrow
        self.__get_habits()
        self.__record_habit_progress(300)

        # [then] level change == 1
        record = self.__get_record_by_index(-1)
        self.assertEqual(record.get("level_change"), 1)

        # [when] on the next day, record progress by 330
        after_two_days = tomorrow + timedelta(days=1)
        mocked_datetime.now.return_value = after_two_days
        self.__get_habits()
        self.__record_habit_progress(330)

        # [then] level change == 1
        record = self.__get_record_by_index(-1)
        self.assertEqual(record.get("level_change"), 1)

    @mock.patch("account.models_aux.datetime", wraps=datetime)
    def test_daily_record_xp_accumulate(self, mocked_datetime):
        # [setup] initialize habit
        habit = Habit.objects.get(pk=self.habit_id)
        habit.day_cycle = 1
        habit.save()

        # [given] on the first day, xp accumulate == 60
        self.__record_habit_progress(60)
        record = self.__get_first_record()
        self.assertEqual(record.get("xp_accumulate"), 60)

        # [when] on the next day
        tomorrow = datetime.today() + timedelta(days=1)
        mocked_datetime.now.return_value = tomorrow
        self.__get_habits()

        # [then] xp accumulate == 60
        record = self.__get_record_by_index(-1)
        self.assertEqual(record.get("xp_accumulate"), 60)

        # [when] record progress by 70
        self.__record_habit_progress(70)

        # [then] xp_accumulate == 130
        record = self.__get_record_by_index(-1)
        self.assertEqual(record.get("xp_accumulate"), 130)

        # [when] on the next day, record progress by 80
        after_two_days = tomorrow + timedelta(days=1)
        mocked_datetime.now.return_value = after_two_days
        self.__get_habits()
        self.__record_habit_progress(80)

        # [then] xp_accumulate == 210
        record = self.__get_record_by_index(-1)
        self.assertEqual(record.get("xp_accumulate"), 210)

    @mock.patch("account.models_aux.datetime", wraps=datetime)
    def test_daily_record_xp_change(self, mocked_datetime):
        # [setup] initialize habit
        habit = Habit.objects.get(pk=self.habit_id)
        habit.day_cycle = 1
        habit.save()

        # [given] on the first day, xp accumulate == 60
        self.__record_habit_progress(60)
        record = self.__get_first_record()
        self.assertEqual(record.get("xp_accumulate"), 60)

        # [given] on the next day, skip habit
        tomorrow = datetime.today() + timedelta(days=1)
        mocked_datetime.now.return_value = tomorrow
        self.__get_habits()

        # [when] on the next day, XP decreases
        after_two_days = tomorrow + timedelta(days=1)
        mocked_datetime.now.return_value = after_two_days
        self.__get_habits()

        # [then] xp_accumulate == 30
        record = self.__get_record_by_index(-1)
        self.assertEqual(record.get("xp_accumulate"), 30)

    def test_daily_record_updated_when_round_finished(self):
        self.__record_habit_progress(60)
        record = self.__get_first_record()
        self.assertEqual(record.get("xp_accumulate"), 60)
        self.assertEqual(record.get("xp_change"), 60)

    def test_daily_record_updated_when_round_finished_continuously(self):
        # [given]
        # habit's initial goal == 300
        # habit's growth amount == 30
        habit = self.__get_habit()
        self.assertEqual(habit.get("goal_xp"), 300)
        self.assertEqual(habit.get("growth_amount"), 30)

        # [given] record by 60 seconds
        self.__record_habit_progress(60)

        # [when] adding 200 seconds
        self.__record_habit_progress(200)
        record = self.__get_first_record()
        # [then] total 260 seconds
        self.assertEqual(record.get("xp_accumulate"), 260)
        self.assertEqual(record.get("xp_change"), 260)

        # [when] adding 150 seconds
        self.__record_habit_progress(150)
        record = self.__get_first_record()
        # [then] level increased & xp subtracted
        self.assertEqual(record.get("level_now"), 2)
        self.assertEqual(record.get("level_change"), 1)
        self.assertEqual(record.get("xp_accumulate"), 410)
        self.assertEqual(record.get("xp_change"), 410)

    def __get_records(self) -> list[DailyRecordType]:
        response = self.client.get(
            f"/api/habit/{self.habit_id}/record/", **self.auth_headers
        )
        data: list[DailyRecordType] = response.json()
        return data

    def __get_first_record(self) -> DailyRecordType:
        return self.__get_record_by_index(0)

    def __get_record_by_index(self, index) -> DailyRecordType:
        return self.__get_records()[index]

    def __get_habits(self) -> None:
        self.client.get("/api/habit/", **self.auth_headers)

    def __get_habit(self) -> HabitReadType:
        response = self.client.get(f"/api/habit/{self.habit_id}/", **self.auth_headers)
        data: HabitReadType = response.json()
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
