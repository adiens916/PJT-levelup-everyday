from datetime import datetime, time, timedelta

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from rest_framework.request import Request

from .models_aux import DateTimeCalculator


class User(AbstractUser):
    next_reset_date = models.DateField(blank=True, null=True)
    daily_reset_time = models.TimeField(default=time(hour=0, minute=0))
    is_recording = models.BooleanField(default=False)

    objects = UserManager()

    @staticmethod
    def create_from_request(request: Request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        user: User = __class__.objects.create_user(username, email, password)
        return user

    def change_standard_reset_time(self, request: Request) -> None:
        standard_reset_time = request.data.get("standard_reset_time")
        if not standard_reset_time:
            raise ValueError("No data in request")

        matched = DateTimeCalculator.is_iso_format(standard_reset_time)
        if not matched:
            raise ValueError(
                f"Time format must be ISO format (HH:MM), \
                    but given time format is ({time})"
            )

        hour, minute = standard_reset_time.split(":")
        self.daily_reset_time = time(int(hour), int(minute))

    def is_day_changed(self):
        if self.next_reset_date == None:
            return True

        return self.get_reset_datetime() <= datetime.now()

    def get_yesterday(self):
        return self.get_reset_datetime().date() - timedelta(days=1)

    def get_today(self):
        return datetime.now().date()

    def get_reset_datetime(self):
        reset_datetime = datetime.combine(self.next_reset_date, self.daily_reset_time)
        return reset_datetime
