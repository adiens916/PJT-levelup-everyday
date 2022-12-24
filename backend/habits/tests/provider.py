from django.test import Client
from account.models import User

USERNAME = "john"
PASSWORD = "doe"
HABIT_INFO = {
    "name": "Reading a book",
    "estimate_type": "TIME",
    "estimate_unit": "",
    "final_goal": 3600,
    "growth_type": "INCREASE",
    "day_cycle": 2,
    "initial_goal": 300,
}


class TestDataProvider:
    def __init__(self) -> None:
        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD)

    def get_auth_headers(self) -> dict:
        credentials = {"username": USERNAME, "password": PASSWORD}
        response = Client().post("/api/account/login/", credentials)

        items: dict = response.json()
        token = items.get("token")
        return {"HTTP_AUTHORIZATION": f"Token {token}"}

    def create_habit(self) -> int:
        response = Client().post(
            "/api/habit/", data=HABIT_INFO, **self.get_auth_headers()
        )

        items: dict = response.json()
        habit_id = items.get("id")
        return habit_id
