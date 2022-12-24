from django.test import TestCase

from habits.models import Habit
from .provider import TestDataProvider


class HabitViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        provider = TestDataProvider()
        cls.auth_headers = provider.get_auth_headers()
        cls.habit_id = provider.create_habit()
        provider.create_habits()

    def test_create_habit(self):
        habit = Habit.objects.get(pk=self.habit_id)
        self.assertEqual(habit.name, "Reading a book")
        self.assertEqual(habit.final_goal, 3600)
        self.assertEqual(habit.goal_xp, 300)

    def test_get_habits(self):
        pass

    def test_get_a_habit(self):
        pass

    def test_delete_habit(self):
        pass

    def test_update_importance(self):
        pass

    def test_get_daily_records(self):
        pass
