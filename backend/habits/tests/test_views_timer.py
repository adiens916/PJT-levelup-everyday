from datetime import date, datetime, time, timedelta
from unittest import expectedFailure

from django.test import TestCase

from habits.models import Habit, RoundRecord
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

    def test_start_timer(self):
        before = datetime.now()
        self.__start_timer()
        after = datetime.now()

        habit = Habit.objects.get(pk=self.habit_id)
        self.assertTrue(habit.is_running)

        self.assertIsInstance(habit.start_datetime, datetime)
        self.assertGreaterEqual(habit.start_datetime, before - timedelta(minutes=1))
        self.assertLessEqual(habit.start_datetime, after + timedelta(minutes=1))

    @expectedFailure
    def test_failed_start_timer_when_already_running(self):
        habit = Habit.objects.get(pk=self.habit_id)
        self.assertTrue(habit.is_running)

        with self.assertRaises(Exception):
            self.__start_timer()

    def test_finish_timer(self):
        self.__start_timer()

        habit = Habit.objects.get(pk=self.habit_id)
        self.assertTrue(habit.is_running)

        self.__finish_timer(45)

        round_record = RoundRecord.objects.get(habit=habit)
        self.assertEqual(round_record.progress, 45)

        habit = Habit.objects.get(pk=self.habit_id)
        self.assertEqual(habit.goal_xp, 300)
        self.assertEqual(habit.current_xp, 45)

    def test_finish_timer_when_level_up(self):
        self.__start_timer()

        habit = Habit.objects.get(pk=self.habit_id)
        self.assertTrue(habit.is_running)

        habit.growth_amount = 60
        habit.save()

        self.__finish_timer(450)

        round_record = RoundRecord.objects.get(habit=habit)
        self.assertEqual(round_record.progress, 450)

        habit = Habit.objects.get(pk=self.habit_id)
        self.assertEqual(habit.goal_xp, 360)
        self.assertEqual(habit.current_xp, 150)

    def test_finish_timer_when_level_up_a_lot(self):
        # [given] (growth amount == 60)
        # lv.1: 0 / 300
        # lv.2: 0 / 360 (300 + 60)
        # lv.3: 0 / 420 (360 + 60)
        # lv.4: 0 / 480 (420 + 60)

        habit = Habit.objects.get(pk=self.habit_id)
        habit.growth_amount = 60
        habit.save()

        # [when] given 900 XP

        self.__start_timer()
        self.__finish_timer(900)

        # [then]
        # lv.1: 900 / 300 => lv.2
        # lv.2: 600 / 360 => lv.3
        # lv.3: 240 / 420

        habit = Habit.objects.get(pk=self.habit_id)
        self.assertEqual(habit.goal_xp, 420)
        self.assertEqual(habit.current_xp, 240)

    def __start_timer(self) -> None:
        self.client.post(
            "/api/habit/timer/start/", {"habit_id": self.habit_id}, **self.auth_headers
        )

    def __finish_timer(self, progress: int) -> None:
        self.client.post(
            "/api/habit/timer/finish/",
            {"habit_id": self.habit_id, "progress": progress},
            **self.auth_headers,
        )
