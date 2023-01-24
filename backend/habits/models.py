from datetime import date, timedelta

from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Sum

from rest_framework.request import Request
from account.models import User

ESTIMATE_TYPE_CHOICES = [("TIME", "TIME"), ("COUNT", "COUNT")]
GROWTH_TYPE_CHOICES = [("INCREASE", "INCREASE"), ("DECREASE", "DECREASE")]


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
        self.__set_initial_goal_xp(request)
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

    def start_recording(self, should_change_user_record_state=True):
        self.start_datetime = timezone.now()
        self.is_running = True
        self.save()

        if should_change_user_record_state:
            user: User = self.user
            user.is_recording = True
            user.save()

    def end_recording(self, progress: int, should_change_user_record_state=True):
        self.start_datetime = None
        self.is_running = False
        self.current_xp += progress
        self.use_xp_for_level_up()
        # 'is_done' will be reset when updating due date.
        self.is_done = True
        self.save()

        if should_change_user_record_state:
            user: User = self.user
            user.is_recording = False
            user.save()

    def use_xp_for_level_up(self):
        while self.current_xp >= self.goal_xp:
            self.current_xp -= self.goal_xp
            self.goal_xp += self.growth_amount
            self.level += 1

    def lose_xp(self) -> int:
        steps_for_losing_xp = (
            self.__lose_xp_if_current_xp_is_enough,
            self.__lose_xp_with_level_down,
            self.__lose_xp_if_goal_xp_is_not_enough,
        )

        for step in steps_for_losing_xp:
            decrease_amount = step()
            if decrease_amount != None:
                return decrease_amount

    def __lose_xp_if_current_xp_is_enough(self) -> int | None:
        decrease_amount = int(self.goal_xp * 0.1)
        if self.current_xp >= decrease_amount:
            self.current_xp -= decrease_amount
            return decrease_amount
        else:
            return None

    def __lose_xp_with_level_down(self) -> int | None:
        if self.goal_xp > self.growth_amount:
            self.goal_xp -= self.growth_amount

            new_decrease_amount = int(self.goal_xp * 0.1)
            self.current_xp = self.goal_xp - new_decrease_amount

            if self.level > 1:
                self.level -= 1

            return new_decrease_amount
        else:
            return None

    def __lose_xp_if_goal_xp_is_not_enough(self) -> int | None:
        decrease_amount = self.current_xp
        self.current_xp = 0
        return decrease_amount

    def update_due(self):
        user: User = self.user
        if self.is_due_or_done():
            # due date should be reset as today for habit done but not due
            self.due_date = user.get_day_on_progress()
            self.due_date += timedelta(days=self.day_cycle)
            self.is_done = False

        if self.due_date <= user.get_day_to_proceed():
            self.is_today_due_date = True
        else:
            self.is_today_due_date = False

    def is_due_or_done(self):
        return self.is_today_due_date or self.is_running or self.is_done

    def is_owned_by_user(self, given_user: User):
        return self.user.pk == given_user.pk


class RoundRecord(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    progress = models.PositiveIntegerField()

    def create_from_habit_finished(self, habit: Habit, progress: int | float):
        user: User = habit.user

        self.habit = habit
        self.date = user.get_day_on_progress()
        self.start_datetime = habit.start_datetime

        self.end_datetime = timezone.now()
        self.progress = int(progress)
        self.save()

    def create_from_habit_running(self, habit: Habit):
        user: User = habit.user

        self.habit = habit
        self.date = user.get_day_on_progress()
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
    xp_change = models.IntegerField()
    xp_accumulate = models.IntegerField()

    @staticmethod
    def get_today_record(habit: Habit):
        user: User = habit.user
        try:
            daily_record = DailyRecord.objects.get(
                habit=habit.pk, date=user.get_day_on_progress()
            )
            return daily_record
        except DailyRecord.DoesNotExist:
            return None

    @staticmethod
    def create_or_update_from_habit(habit: Habit) -> None:
        user: User = habit.user
        try:
            daily_record = DailyRecord.objects.get(
                habit=habit.pk, date=user.get_day_on_progress()
            )
        except DailyRecord.DoesNotExist:
            DailyRecord().create_from_habit(habit)
        else:
            daily_record.update_from_habit(habit)

    def create_from_habit(self, habit: Habit, is_for_new_day=False):
        user: User = habit.user

        self.habit = habit
        if is_for_new_day:
            self.date = user.get_day_to_proceed()
        else:
            self.date = user.get_day_on_progress()

        self.update_from_habit(habit)

    def update_from_habit(self, habit: Habit, xp_change=0):
        self.success = habit.is_done

        self.level_now = habit.level
        self.level_change = self.__calc_level_change()
        self.xp_change = self.__calc_xp_change() if not xp_change else xp_change
        self.xp_accumulate = self.__calc_xp_accumulate()

        self.save()

    def __calc_level_change(self) -> int:
        previous_record = self.__get_previous_record()
        if not previous_record:
            return self.level_now - 1
        else:
            return self.level_now - previous_record.level_now

    def __calc_xp_change(self) -> int:
        round_records = RoundRecord.objects.filter(habit=self.habit, date=self.date)
        today_progress_sum = round_records.aggregate(Sum("progress")).get(
            "progress__sum"
        )
        return today_progress_sum if today_progress_sum else 0

    def __calc_xp_accumulate(self) -> int:
        previous_record = self.__get_previous_record()
        if not previous_record:
            return self.xp_change
        else:
            return previous_record.xp_accumulate + self.xp_change

    def __get_previous_record(self):
        daily_records = DailyRecord.objects.filter(habit=self.habit.pk)
        if not any(daily_records):
            return None

        daily_records = daily_records.order_by("-date")
        latest_record = daily_records[0]

        if not latest_record.__is_date_equal_to_today():
            return latest_record

        # when record.date == today
        if daily_records.count() > 1:
            latest_record_except_today = daily_records[1]
            return latest_record_except_today
        else:
            # there's only one record, hence no previous ones
            return None

    def __is_date_equal_to_today(self):
        user: User = self.habit.user
        return self.date == user.get_day_to_proceed()
