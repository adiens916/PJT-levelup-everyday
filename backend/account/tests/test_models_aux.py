from unittest import TestCase, mock
from datetime import date, datetime, time

from account.models_aux import DateTimeCalculator


class DateTimeCalculatorTestCase(TestCase):
    def test_is_iso_format(self):
        given_time = "03:30"
        matched = DateTimeCalculator.is_iso_format(given_time)
        self.assertTrue(matched)

        wrong_time = "3:30"
        matched = DateTimeCalculator.is_iso_format(wrong_time)
        self.assertFalse(matched)

    def test_get_relative_date_when_reset_after_midnight(self):
        reset_time = time(2, 0)

        now = datetime(2023, 1, 8, 23, 0)
        relative_date = DateTimeCalculator.get_relative_date(now, reset_time)
        self.assertEqual(relative_date, date(2023, 1, 8))

        now = datetime(2023, 1, 9, 1, 0)
        relative_date = DateTimeCalculator.get_relative_date(now, reset_time)
        self.assertEqual(relative_date, date(2023, 1, 8))

        now = datetime(2023, 1, 9, 2, 0)
        relative_date = DateTimeCalculator.get_relative_date(now, reset_time)
        self.assertEqual(relative_date, date(2023, 1, 9))

        now = datetime(2023, 1, 9, 3, 0)
        relative_date = DateTimeCalculator.get_relative_date(now, reset_time)
        self.assertEqual(relative_date, date(2023, 1, 9))

        now = datetime(2023, 1, 9, 14, 0)
        relative_date = DateTimeCalculator.get_relative_date(now, reset_time)
        self.assertEqual(relative_date, date(2023, 1, 9))

    def test_get_relative_date_when_reset_before_midnight(self):
        reset_time = time(22, 0)

        now = datetime(2023, 1, 8, 20, 0)
        relative_date = DateTimeCalculator.get_relative_date(now, reset_time)
        self.assertEqual(relative_date, date(2023, 1, 8), "2023-01-08 20:00")

        now = datetime(2023, 1, 8, 22, 0)
        relative_date = DateTimeCalculator.get_relative_date(now, reset_time)
        self.assertEqual(relative_date, date(2023, 1, 9), "2023-01-08 22:00")

        now = datetime(2023, 1, 8, 23, 0)
        relative_date = DateTimeCalculator.get_relative_date(now, reset_time)
        self.assertEqual(relative_date, date(2023, 1, 9), "2023-01-08 23:00")

        now = datetime(2023, 1, 9, 2, 0)
        relative_date = DateTimeCalculator.get_relative_date(now, reset_time)
        self.assertEqual(relative_date, date(2023, 1, 9), "2023-01-09 02:00")

        now = datetime(2023, 1, 9, 7, 0)
        relative_date = DateTimeCalculator.get_relative_date(now, reset_time)
        self.assertEqual(relative_date, date(2023, 1, 9), "2023-01-09 07:00")

        now = datetime(2023, 1, 9, 13, 0)
        relative_date = DateTimeCalculator.get_relative_date(now, reset_time)
        self.assertEqual(relative_date, date(2023, 1, 9), "2023-01-09 13:00")
