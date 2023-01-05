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

    def test_check_authenticated(self):
        credentials = {"username": "john", "password": "doe"}
        response = self.client.post("/api/account/login/", credentials)

        items: dict = response.json()
        token = items.get("token")
        print("token: ", token)

        # NOTE: Headers should be in upper case (capital letters).
        headers = {"HTTP_AUTHORIZATION": f"Token {token}"}
        response = self.client.post("/api/account/check-auth/", **headers)
        # print(response.content)
        # print("< response >")
        # print(*response.items(), sep="\n")

        self.assertContains(response, "id")
        self.assertContains(response, "name")
