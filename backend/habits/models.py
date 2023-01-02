from datetime import date, datetime, timedelta
from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator
from django.utils import timezone
from rest_framework.request import Request
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

    level = models.PositiveIntegerField(default=1)
    goal_xp = models.PositiveIntegerField(default=0)
    current_xp = models.PositiveIntegerField(default=0)
    growth_amount = models.IntegerField(default=0)
    due_date = models.DateField(default=date.today)
    is_today_due_date = models.BooleanField(default=True)
    is_done = models.BooleanField(default=False)  # Added for front-end

    is_running = models.BooleanField(default=False)
    start_datetime = models.DateTimeField(null=True, blank=True)
    is_paused = models.BooleanField(default=False)
    paused_datetime = models.DateTimeField(null=True, blank=True)
    temporary_progress = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.name

    def create_from_request(self, request: Request):
        self.user = request.user
        self.name = request.data.get("name")

        self.estimate_type = request.data.get("estimate_type")
        self.estimate_unit = request.data.get("estimate_unit")
        self.final_goal = int(request.data.get("final_goal"))
        self.growth_type = request.data.get("growth_type")
        self.day_cycle = int(request.data.get("day_cycle"))

        self.__modify_final_goal_by_unit()
        self.goal_xp = self.__set_initial_goal_xp(request)
        self.growth_amount = self.__set_initial_growth_amount(self.final_goal)
        self.save()

    def __modify_final_goal_by_unit(self):
        if self.estimate_type == "TIME":
            if self.estimate_unit == "HOUR":
                self.final_goal *= 3600
            elif self.estimate_unit == "MINUTE":
                self.final_goal *= 60

    def __set_initial_goal_xp(self, request: Request):
        initial_goal = request.data.get("initial_goal")
        if initial_goal:
            self.goal_xp = int(initial_goal)
        else:
            self.goal_xp = int(self.final_goal * 0.01)

    def __set_initial_growth_amount(self, final_goal: int):
        initial_growth_amount = int(final_goal * 0.01)
        if 0 <= initial_growth_amount < 30:
            return 10
        elif 30 <= initial_growth_amount < 60:
            return 30
        else:
            return (initial_growth_amount // 60) * 60

    def start_recording(self):
        self.start_datetime = timezone.now()
        self.is_running = True
        self.save()

        user: User = self.user
        user.is_recording = True
        user.save()

    def end_recording(self, progress: int, save=True):
        self.start_datetime = None
        self.is_running = False
        self.current_xp += progress
        self.use_xp_for_level_up()
        self.is_done = True
        # 'is_done' will be reset as False
        # by DueAdjuster when day changes.

        if save:
            self.save()

        user: User = self.user
        user.is_recording = False
        user.save()

    def use_xp_for_level_up(self):
        while self.current_xp >= self.goal_xp:
            self.current_xp -= self.goal_xp
            self.goal_xp += self.growth_amount
            self.level += 1

    def lose_xp(self):
        decrease_amount = int(self.goal_xp * 0.1)

        if self.current_xp >= decrease_amount:
            self.current_xp -= decrease_amount
        elif self.goal_xp > self.growth_amount:
            self.level -= 1
            self.goal_xp -= self.growth_amount
            decrease_amount = int(self.goal_xp * 0.1)
            self.current_xp = self.goal_xp - decrease_amount
        else:
            self.current_xp = 0

    def is_due_or_done(self):
        return self.is_today_due_date or self.is_running or self.is_done

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
    level_now = models.PositiveIntegerField()
    level_change = models.IntegerField()
    xp_now = models.PositiveIntegerField()
    xp_change = models.IntegerField()

    def create_from_habit(self, habit: Habit):
        user: User = habit.user

        self.habit = habit
        self.date = user.get_yesterday()
        self.success = habit.is_done

        self.level_now = habit.level
        self.level_change = self.calc_level_change()
        self.xp_now = habit.current_xp
        self.xp_change = self.calc_xp_change()

        self.save()

    def calc_level_change(self):
        try:
            latest = DailyRecord.objects.latest("date")
            return self.level_now - latest.level_now
        except Exception:
            # If it's the first record, there is no previous record.
            # The level starts from not 0 but 1
            return self.level_now - 1

    def calc_xp_change(self):
        try:
            latest = DailyRecord.objects.latest("date")
            return self.xp_now - latest.xp_now
        except Exception:
            return self.xp_now

    def is_owned_by_user(self, given_user: User):
        return self.habit.is_owned_by_user(given_user)
