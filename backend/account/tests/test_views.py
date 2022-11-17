from unittest import mock

from django.test import TestCase

from account.models import User


class HabitViewTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="john", password="doe")

    def test_login(self):
        response = self.client.post(
            "/api/account/login/", {"username": "john", "password": "doe"}
        )
        print(response.content)
