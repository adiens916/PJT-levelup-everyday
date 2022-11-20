from datetime import date, datetime, timedelta
from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator
from django.http import HttpRequest
from django.utils import timezone
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

    goal_xp = models.PositiveIntegerField(default=0)
    current_xp = models.PositiveIntegerField(default=0)
    growth_amount = models.IntegerField(default=0)
    due_date = models.DateField(default=date.today)
    is_today_due_date = models.BooleanField(default=True)

    is_running = models.BooleanField(default=False)
    start_datetime = models.DateTimeField(null=True, blank=True)
    is_paused = models.BooleanField(default=False)
    paused_datetime = models.DateTimeField(null=True, blank=True)
    temporary_progress = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.name

    def create_from_request(self, request: HttpRequest):
        self.user = request.user
        self.name = request.POST.get("name")

        self.estimate_type = request.POST.get("estimate_type")
        self.estimate_unit = request.POST.get("estimate_unit")
        self.final_goal = int(request.POST.get("final_goal"))
        self.growth_type = request.POST.get("growth_type")
        self.day_cycle = int(request.POST.get("day_cycle"))

        if self.growth_type == "INCREASE":
            initial_goal = request.POST.get("initial_goal")
            if initial_goal:
                self.goal_xp = int(initial_goal)
            else:
                self.goal_xp = self.get_initial_today_goal(self.final_goal)
            self.growth_amount = self.get_initial_growth_amount(self.final_goal)
        elif self.growth_type == "DECREASE":
            self.goal_xp = int(self.final_goal * 10)
            self.growth_amount = int((self.goal_xp - self.final_goal) * 0.01)
        self.save()

    def get_initial_today_goal(self, final_goal: int):
        thresholds = [0, 10, 15, 20, 60]
        goals = [0.5, 1, 3, 5, 10]

        final_goal_as_minute = final_goal // 60
        try:
            for i in range(len(thresholds)):
                if thresholds[i] <= final_goal_as_minute < thresholds[i + 1]:
                    today_goal = goals[i]
                    break
        except:
            today_goal = goals[-1]
        finally:
            return int(today_goal * 60)

    def get_initial_growth_amount(self, final_goal: int):
        initial_growth_amount = int(final_goal * 0.01)
        if 0 <= initial_growth_amount < 30:
            return 10
        elif 30 <= initial_growth_amount < 60:
            return 30
        else:
            return (initial_growth_amount // 60) * 60

    def save_start_datetime(self):
        self.start_datetime = timezone.now()
        self.is_running = True
        self.save()

        user: User = self.user
        user.is_recording = True
        user.save()

    def add_progress_and_init(self, progress: int, save=True):
        self.start_datetime = None
        self.is_running = False
        self.current_xp += progress
        if save:
            self.save()

        user: User = self.user
        user.is_recording = False
        user.save()

    def is_due_or_done(self):
        return self.is_today_due_date or self.current_xp > 0 or self.is_running

    def is_today_successful(self) -> bool:
        if self.growth_type == "INCREASE":
            return self.goal_xp <= self.current_xp
        elif self.growth_type == "DECREASE":
            return self.goal_xp >= self.current_xp

    def is_owned_by_user(self, given_user: User):
        return self.user.pk == given_user.pk


class RoundRecord(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    progress = models.PositiveIntegerField()

    def create_from_habit_finished(self, habit: Habit, progress: int | float):
        self.habit = habit
        self.start_datetime = habit.start_datetime

        self.end_datetime = timezone.now()
        self.progress = int(progress)
        self.save()

    def create_from_habit_running(self, habit: Habit):
        self.habit = habit
        self.start_datetime = habit.start_datetime

        user: User = self.habit.user
        reset_datetime = user.get_reset_datetime()
        self.end_datetime = reset_datetime - timedelta(minutes=1)

        # TIME 유형인 경우, 현재 시각을 끝으로 진행도 결정
        if habit.estimate_type == "TIME":
            diff: timedelta = self.end_datetime - self.start_datetime
            self.progress = int(diff.total_seconds())
        elif habit.estimate_type == "COUNT":
            self.progress = habit.temporary_progress
        self.save()


class DailyRecord(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    success = models.BooleanField()
    goal = models.PositiveIntegerField()
    progress = models.PositiveIntegerField()
    excess = models.PositiveIntegerField()

    def create_from_habit(self, habit: Habit):
        user: User = habit.user

        self.habit = habit
        self.date = user.get_yesterday()
        self.success = habit.is_today_successful()
        self.set_record_by_success_and_growth_type(habit)
        self.save()

    def set_record_by_success_and_growth_type(self, habit: Habit):
        if self.success:
            if habit.growth_type == "INCREASE":
                self.set_for_excess(habit)
            elif habit.growth_type == "DECREASE":
                self.set_for_lack(habit)
        else:
            if habit.growth_type == "INCREASE":
                self.set_for_lack(habit)
            elif habit.growth_type == "DECREASE":
                self.set_for_excess(habit)

    def set_for_excess(self, habit: Habit):
        self.goal = habit.goal_xp
        self.progress = habit.goal_xp
        self.excess = habit.current_xp

    def set_for_lack(self, habit: Habit):
        self.goal = habit.goal_xp
        self.progress = habit.current_xp
        self.excess = 0

    def is_owned_by_user(self, given_user: User):
        return self.habit.is_owned_by_user(given_user)
