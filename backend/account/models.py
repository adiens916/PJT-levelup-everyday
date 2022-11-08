from datetime import datetime, time, timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http import HttpRequest

# Create your models here.
class User(AbstractUser):
    next_reset_date = models.DateField(blank=True, null=True)
    daily_reset_time = models.TimeField(default=time(hour=0, minute=0))
    is_recording = models.BooleanField(default=False)

    @staticmethod
    def create_from_request(request: HttpRequest):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user: User = __class__.objects.create_user(username, email, password)
        return user

    def change_standard_reset_time(self, request: HttpRequest) -> None:
        standard_reset_time = request.POST.get("standard_reset_time")
        # ex) '03:30'
        # TODO: 정규표현식으로 체크하기
        if standard_reset_time:
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
