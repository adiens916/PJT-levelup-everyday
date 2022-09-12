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

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    estimate_type = models.CharField(max_length=10, choices=ESTIMATE_TYPE_CHOICES)
    estimate_unit = models.CharField(max_length=10, blank=True)
    final_goal = models.PositiveIntegerField()
    growth_type = models.CharField(max_length=10, choices=GROWTH_TYPE_CHOICES)
    day_cycle = models.PositiveSmallIntegerField(default=0)
    
    today_goal = models.PositiveIntegerField(null=True, blank=True)
    today_progress = models.PositiveIntegerField(null=True, blank=True)
    growth_amount = models.IntegerField(null=True, blank=True)
    last_done_date = models.DateTimeField(null=True, blank=True)

    is_running = models.BooleanField(default=False)
    is_paused = models.BooleanField(default=False)
    start_date = models.DateTimeField(null=True, blank=True)
    paused_date = models.DateTimeField(null=True, blank=True)
    temporary_progress = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class RoundRecord(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    progress = models.PositiveIntegerField()

class DailyRecord(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateTimeField()
    goal = models.PositiveIntegerField()
    progress = models.PositiveIntegerField()
    success = models.BooleanField()