from unittest import mock

from django.test import TestCase

from account.models import User


class AccountViewTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="john", password="doe")

    def test_login(self):
        credentials = {"username": "john", "password": "doe"}
        response = self.client.post("/api/account/login/", credentials)
        # print(response.client)

        items: dict = response.json()
        self.assertTrue(items.get("token"))
        self.assertTrue(items.get("user_id"))
        self.assertIsNone(items.get("success"))
