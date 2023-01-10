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

    @mock.patch("account.models_aux.datetime", wraps=datetime)
    def test_is_day_changed_relatively_when_reset_after_midnight(self, mocked_datetime):
        # [given]
        # it has been updated at 2023-01-10
        # and it is reset at 2:00 AM
        reset_time = time(2, 0)
        last_reset_date = date(2023, 1, 10)

        # [when] now is 2023-01-11 00:00 AM
        now = datetime(2023, 1, 11, 0, 0)
        mocked_datetime.now.return_value = now

        # [then] today is 2023-01-10 relatively, though 2023-01-11 absolutely
        result = DateTimeCalculator.is_day_changed_relatively(
            last_reset_date, reset_time
        )
        self.assertFalse(result)

        now = datetime(2023, 1, 11, 2, 0)
        mocked_datetime.now.return_value = now

        result = DateTimeCalculator.is_day_changed_relatively(
            last_reset_date, reset_time
        )
        self.assertTrue(result)

    @mock.patch("habits.models_aux.datetime", wraps=datetime)
    def test_is_day_on_due_relatively(self, mocked_datetime):
        last_done_date = date(2023, 1, 10)
        reset_time = time(2, 0)
        day_cycle = 2

        mocked_datetime.now.return_value = datetime(2023, 1, 11, 2, 0)
        result = DateTimeCalculator.is_day_on_due_relatively(
            last_done_date, reset_time, day_cycle
        )
        self.assertFalse(result)

        mocked_datetime.now.return_value = datetime(2023, 1, 12, 0, 0)
        result = DateTimeCalculator.is_day_on_due_relatively(
            last_done_date, reset_time, day_cycle
        )
        self.assertFalse(result)

        mocked_datetime.now.return_value = datetime(2023, 1, 12, 2, 0)
        result = DateTimeCalculator.is_day_on_due_relatively(
            last_done_date, reset_time, day_cycle
        )
        self.assertTrue(result)
