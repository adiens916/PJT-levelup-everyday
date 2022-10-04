from datetime import time, datetime
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    next_reset_date = models.DateField(blank=True, null=True)
    daily_reset_time = models.TimeField(default=time(hour=0, minute=0))
    is_recording = models.BooleanField(default=False)

    def get_reset_datetime(self):
        reset_datetime = datetime.combine(self.next_reset_date, self.daily_reset_time)
        return reset_datetime
