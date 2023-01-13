from django.test import Client

from account.models import User
from habits.models_type import HabitCreateType

USERNAME = "john"
PASSWORD = "doe"

HABIT_INFO: HabitCreateType = {
    "name": "Reading a book",
    "estimate_type": "TIME",
    "estimate_unit": "",
    "final_goal": 3600,
    "growth_type": "INCREASE",
    "day_cycle": 2,
    "initial_goal": 300,
}
HABIT_INFO_2: HabitCreateType = {
    "name": "Exercise",
    "estimate_type": "TIME",
    "estimate_unit": "",
    "final_goal": 1800,
    "growth_type": "INCREASE",
    "day_cycle": 3,
    "initial_goal": "",
}
HABIT_INFO_3: HabitCreateType = {
    "name": "Study",
    "estimate_type": "TIME",
    "estimate_unit": "",
    "final_goal": 2700,
    "growth_type": "INCREASE",
    "day_cycle": 1,
    "initial_goal": "",
}


class TestDataProvider:
    def __init__(self) -> None:
        self.user: User = User.objects.create_user(username=USERNAME, password=PASSWORD)
        self.__auth_headers = None

    def get_auth_headers(self) -> dict:
        if not self.__auth_headers:
            credentials = {"username": USERNAME, "password": PASSWORD}
            response = Client().post("/api/account/login/", credentials)

            items: dict = response.json()
            token = items.get("token")

            self.__auth_headers = {"HTTP_AUTHORIZATION": f"Token {token}"}

        return self.__auth_headers

    def create_habit(self, **kwargs) -> int:
        response = Client().post(
            "/api/habit/", data={**HABIT_INFO, **kwargs}, **self.get_auth_headers()
        )

        items: dict = response.json()
        habit_id = items.get("id")
        return habit_id

    def create_habits(self) -> None:
        for habit_info in (HABIT_INFO_2, HABIT_INFO_3):
            Client().post("/api/habit/", data=habit_info, **self.get_auth_headers())
