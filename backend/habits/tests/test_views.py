from django.test import TestCase

from habits.models import Habit
from .provider import TestDataProvider


class HabitViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        provider = TestDataProvider()
        cls.auth_headers = provider.get_auth_headers()
        cls.habit_id = provider.create_habit()

    def test_create_habit(self):
        habit = Habit.objects.get(pk=self.habit_id)
        self.assertEqual(habit.name, "Reading a book")
        self.assertEqual(habit.final_goal, 3600)
        self.assertEqual(habit.goal_xp, 300)
