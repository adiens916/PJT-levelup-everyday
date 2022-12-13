import re
from datetime import datetime, time, timedelta

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.http import HttpRequest

# Create your models here.
class User(AbstractUser):
    next_reset_date = models.DateField(blank=True, null=True)
    daily_reset_time = models.TimeField(default=time(hour=0, minute=0))
    is_recording = models.BooleanField(default=False)

    objects = UserManager()

    @staticmethod
    def create_from_request(request: HttpRequest):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user: User = __class__.objects.create_user(username, email, password)
        return user

    def change_standard_reset_time(self, request: HttpRequest) -> None:
        standard_reset_time = request.POST.get("standard_reset_time")
        if not standard_reset_time:
            return

        # Ex.) '03:30'
        time_pattern = "([0-1][0-9]|2[0-3]):([0-5][0-9])"
        matched = re.match(time_pattern, standard_reset_time)
        if not matched:
            return

        hour, minute = standard_reset_time.split(":")
        self.daily_reset_time = time(int(hour), int(minute))

    def is_day_changed(self):
        if self.next_reset_date == None:
            return True

        return self.get_reset_datetime() <= datetime.now()

    def get_yesterday(self):
        return self.get_reset_datetime().date() - timedelta(days=1)

    def get_reset_datetime(self):
        reset_datetime = datetime.combine(self.next_reset_date, self.daily_reset_time)
        return reset_datetime
