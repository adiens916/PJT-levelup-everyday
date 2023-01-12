from datetime import datetime, time, timedelta

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from rest_framework.request import Request

from .models_aux import RelativeDateTime, is_iso_format_time


class User(AbstractUser):
    last_reset_date = models.DateField(blank=True, null=True)
    reset_time = models.TimeField(default=time(hour=0, minute=0))
    is_recording = models.BooleanField(default=False)

    objects = UserManager()

    @staticmethod
    def create_from_request(request: Request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        user: User = __class__.objects.create_user(username, email, password)

        user.change_standard_reset_time(request)
        user.last_reset_date = RelativeDateTime.get_relative_date(
            datetime.now(), user.reset_time
        )

        user.save()
        return user

    def change_standard_reset_time(self, request: Request) -> None:
        standard_reset_time = request.data.get("standard_reset_time")
        if not standard_reset_time:
            return

        matched = is_iso_format_time(standard_reset_time)
        if not matched:
            raise ValueError(
                f"Time format must be ISO format (HH:MM), \
                    but given time format is ({time})"
            )

        hour, minute = standard_reset_time.split(":")
        self.reset_time = time(int(hour), int(minute))

    def is_day_changed(self):
        return RelativeDateTime(
            self.last_reset_date, self.reset_time
        ).is_day_changed_relatively()

    def get_day_on_progress(self):
        return self.last_reset_date

    def get_day_to_proceed(self):
        return RelativeDateTime.get_relative_date_for_now(self.reset_time)

    def update_reset_date(self) -> None:
        self.last_reset_date = self.get_day_to_proceed()
        self.save()
