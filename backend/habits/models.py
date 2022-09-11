from django.db import models

# Create your models here.
class Habit(models.Model):
    ESTIMATE_TYPE_CHOICES = [
        ('TIME', 'TIME'),
        ('COUNT', 'COUNT')
    ]

    GROWTH_TYPE_CHOICES = [
        ('INC', 'INCREASE'),
        ('DEC', 'DECREASE')
    ]

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    estimate_type = models.CharField(max_length=10, choices=ESTIMATE_TYPE_CHOICES)
    estimate_unit = models.CharField(max_length=10)
    final_goal = models.PositiveIntegerField()
    growth_type = models.CharField(max_length=10, choices=GROWTH_TYPE_CHOICES)
    day_cycle = models.PositiveSmallIntegerField(default=0)
    
    today_goal = models.PositiveIntegerField()
    today_progress = models.PositiveIntegerField()
    growth_amount = models.IntegerField()
    last_done_date = models.DateTimeField(blank=True)

    is_running = models.BooleanField(default=False)
    is_paused = models.BooleanField(default=False)
    start_date = models.DateTimeField(blank=True)
    paused_date = models.DateTimeField(blank=True)
    temporary_progress = models.PositiveIntegerField()
