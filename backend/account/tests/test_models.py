from datetime import datetime, time, timedelta, date
from unittest import mock

from django.test import TestCase

from account.models import User


class UserModelTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create()

    @mock.patch("account.models.datetime", wraps=datetime)
    def test_is_day_changed_when_reset_at_night(self, mocked_datetime):
        """
        If a user's reset time is PM 10:15, and now is PM 10:30,
        then the day has been changed.
        """

        self.user.next_reset_date = date(2022, 9, 1)
        self.user.daily_reset_time = time(22, 15)
        mocked_datetime.now.return_value = datetime(2022, 9, 1, hour=22, minute=30)
        self.assertIs(self.user.is_day_changed(), True)

    @mock.patch("account.models.datetime", wraps=datetime)
    def test_is_day_changed_when_reset_at_dawn(self, mocked_datetime):
        # given: a user's reset time is AM 06:00
        self.user.next_reset_date = date(2022, 9, 17)
        self.user.daily_reset_time = time(6, 0)

        # when: now is AM 00:00
        mocked_datetime.now.return_value = datetime(2022, 9, 17, hour=0)
        # then: not changed yet
        self.assertIs(self.user.is_day_changed(), False)

        # when: now is AM 07:00
        mocked_datetime.now.return_value = datetime(2022, 9, 17, hour=7)
        # then: changed
        self.assertIs(self.user.is_day_changed(), True)
