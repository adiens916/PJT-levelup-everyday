from datetime import datetime, timedelta

from django.test import TestCase

from habits.models import Habit, RoundRecord
from .provider import TestDataProvider


class HabitViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        provider = TestDataProvider()
        cls.auth_headers = provider.get_auth_headers()
        cls.habit_id = provider.create_habit()

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

    def test_finish_timer_when_level_up(self):
        self.test_start_timer()

        habit = Habit.objects.get(pk=self.habit_id)
        self.assertTrue(habit.is_running)

        habit.growth_amount = 60
        habit.save()

        self.client.post(
            "/api/habit/timer/finish/",
            {"habit_id": self.habit_id, "progress": 450},
            **self.auth_headers,
        )

        round_record = RoundRecord.objects.get(habit=habit)
        self.assertEqual(round_record.progress, 450)

        habit = Habit.objects.get(pk=self.habit_id)
        self.assertEqual(habit.goal_xp, 360)
        self.assertEqual(habit.current_xp, 150)

    def test_finish_timer_when_level_up_a_lot(self):
        """
        lv.1: 0 / 300
        lv.2: 0 / 360
        lv.3: 0 / 420
        lv.4: 0 / 480

        when given 900 XP, then:
        lv.1: 900 / 300 => lv.2
        lv.2: 600 / 360 => lv.3
        lv.3: 240 / 420
        """

        habit = Habit.objects.get(pk=self.habit_id)
        habit.growth_amount = 60
        habit.save()

        self.test_start_timer()
        self.client.post(
            "/api/habit/timer/finish/",
            {"habit_id": self.habit_id, "progress": 900},
            **self.auth_headers,
        )

        habit = Habit.objects.get(pk=self.habit_id)
        self.assertEqual(habit.goal_xp, 420)
        self.assertEqual(habit.current_xp, 240)
