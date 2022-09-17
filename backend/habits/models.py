from django.conf import settings
from django.db import models

ESTIMATE_TYPE_CHOICES = [
    ('TIME', 'TIME'),
    ('COUNT', 'COUNT')
]

GROWTH_TYPE_CHOICES = [
    ('INCREASE', 'INCREASE'),
    ('DECREASE', 'DECREASE')
]

# Create your models here.
class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    estimate_type = models.CharField(max_length=10, choices=ESTIMATE_TYPE_CHOICES)
    estimate_unit = models.CharField(max_length=10, blank=True)
    final_goal = models.PositiveIntegerField()
    growth_type = models.CharField(max_length=10, choices=GROWTH_TYPE_CHOICES)
    day_cycle = models.PositiveSmallIntegerField(default=0)
    
    today_goal = models.PositiveIntegerField(default=0)
    today_progress = models.PositiveIntegerField(default=0)
    growth_amount = models.IntegerField(default=0)
    due_date = models.DateField(null=True, blank=True)
    is_today_due_date = models.BooleanField(default=False)

    is_running = models.BooleanField(default=False)
    start_datetime = models.DateTimeField(null=True, blank=True)
    is_paused = models.BooleanField(default=False)
    paused_datetime = models.DateTimeField(null=True, blank=True)
    temporary_progress = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.name

class RoundRecord(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    progress = models.PositiveIntegerField()

class DailyRecord(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateTimeField()
    goal = models.PositiveIntegerField()
    progress = models.PositiveIntegerField()
    success = models.BooleanField()