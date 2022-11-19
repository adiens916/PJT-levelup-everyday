from unittest import mock

from django.test import TestCase

from account.models import User


class AccountViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="john", password="doe")

    def test_login(self):
        credentials = {"username": "john", "password": "doe"}
        response = self.client.post("/api/account/login/", credentials)
        # print(response.client)

        items: dict = response.json()
        self.assertIsNotNone(items.get("token"))
        self.assertIsNotNone(items.get("user_id"))
        self.assertIsNone(items.get("success"))

    def test_login_failed(self):
        credentials = {"username": "john", "password": "not_password"}
        response = self.client.post("/api/account/login/", credentials)
        # print(response.client)

        items: dict = response.json()
        self.assertIsNone(items.get("token"))
        self.assertIsNone(items.get("user_id"))
        self.assertFalse(items.get("success"))
