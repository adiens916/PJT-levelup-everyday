from unittest import TestCase

from account.models_aux import DateTimeCalculator


class DateTimeCalculatorTestCase(TestCase):
    def test_is_iso_format(self):
        given_time = "03:30"
        matched = DateTimeCalculator.is_iso_format(given_time)
        self.assertIsNotNone(matched)

        wrong_time = "3:30"
        matched = DateTimeCalculator.is_iso_format(wrong_time)
        self.assertIsNone(matched)
