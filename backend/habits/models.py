from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator
from django.http import HttpRequest
from account.models import User

ESTIMATE_TYPE_CHOICES = [("TIME", "TIME"), ("COUNT", "COUNT")]
GROWTH_TYPE_CHOICES = [("INCREASE", "INCREASE"), ("DECREASE", "DECREASE")]

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
    importance = models.PositiveSmallIntegerField(
        default=100, validators=[MaxValueValidator(10000)]
    )

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

    def save_from_request(self, request: HttpRequest):
        self.user = request.user
        self.name = request.POST.get("name")

        self.estimate_type = request.POST.get("estimate_type")
        self.estimate_unit = request.POST.get("estimate_unit")
        self.final_goal = int(request.POST.get("final_goal"))
        self.growth_type = request.POST.get("growth_type")
        self.day_cycle = int(request.POST.get("day_cycle"))

        # 임시로 초기 목표 & 증감량 설정
        if self.growth_type == "INCREASE":
            self.today_goal = int(self.final_goal * 0.01)
            self.growth_amount = int(self.final_goal * 0.01)
        elif self.growth_type == "DECREASE":
            self.today_goal = int(request.POST.get("today_goal"))
            self.growth_amount = int((self.today_goal - self.final_goal) * 0.01)
        self.save()

    def is_owned_by_user(self, given_user: User):
        return self.user.pk == given_user.pk

    def is_today_successful(self) -> bool:
        if self.growth_type == "INCREASE":
            return self.today_goal <= self.today_progress
        elif self.growth_type == "DECREASE":
            return self.today_goal >= self.today_progress


class RoundRecord(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    progress = models.PositiveIntegerField()


class DailyRecord(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    success = models.BooleanField()
    goal = models.PositiveIntegerField()
    progress = models.PositiveIntegerField()
    excess = models.PositiveIntegerField()

    def save_from_habit(self, habit: Habit):
        self.habit = habit
        self.date = habit.due_date
        self.success = habit.is_today_successful()
        if self.success:
            self.goal = habit.today_goal
            self.progress = habit.today_goal
            self.excess = habit.today_progress
        else:
            self.goal = habit.today_goal
            self.progress = habit.today_progress
            self.excess = 0
        self.save()

    def is_owned_by_user(self, given_user: User):
        return self.habit.is_owned_by_user(given_user)
