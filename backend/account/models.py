import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    next_reset_date = models.DateField(blank=True, null=True)
    daily_reset_time = models.TimeField(default=datetime.time(hour=0, minute=0))
    is_recording = models.BooleanField(default=False)
