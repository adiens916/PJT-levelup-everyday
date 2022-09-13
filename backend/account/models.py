from datetime import datetime
from time import time
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class User(AbstractUser):
    last_reset_date = models.DateTimeField(blank=True, null=True)
    standard_reset_time = models.TimeField(default='00:00:00')
    is_recording = models.BooleanField(default=False)