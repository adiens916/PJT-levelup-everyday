from datetime import datetime, time, timedelta, date
from unittest import mock

from django.test import TestCase

from account.models import User


class UserModelTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User()

    @mock.patch("account.models.datetime", wraps=datetime)
    def test_is_day_changed_when_reset_before_midnight(self, mocked_datetime):
        # [given]
        self.user.last_reset_date = date(2022, 9, 1)
        self.user.reset_time = time(22, 15)

        # [when]
        now = datetime(2022, 9, 1, hour=22, minute=30)
        mocked_datetime.now.return_value = now

        # [then]
        self.assertTrue(self.user.is_day_changed())

    @mock.patch("account.models.datetime", wraps=datetime)
    def test_is_day_changed_when_reset_after_midnight(self, mocked_datetime):
        # [given]
        self.user.last_reset_date = date(2022, 9, 17)
        self.user.reset_time = time(2, 0)

        # [when]
        now = datetime(2022, 9, 17, hour=3)
        mocked_datetime.now.return_value = now
        # [then]
        self.assertFalse(self.user.is_day_changed())

        # [when]
        now = datetime(2022, 9, 17, hour=23)
        mocked_datetime.now.return_value = now
        # [then]
        self.assertFalse(self.user.is_day_changed())

        # [when]
        now = datetime(2022, 9, 18, hour=3)
        mocked_datetime.now.return_value = now
        # [then]
        self.assertTrue(self.user.is_day_changed())
