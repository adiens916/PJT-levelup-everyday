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

    today_goal = models.PositiveIntegerField(default=0)
    today_progress = models.PositiveIntegerField(default=0)
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

        # 임시로 초기 목표 & 증감량 설정
        if self.growth_type == "INCREASE":
            self.today_goal = int(self.final_goal * 0.01)
            self.growth_amount = int(self.final_goal * 0.01)
        elif self.growth_type == "DECREASE":
            self.today_goal = int(self.final_goal * 10)
            self.growth_amount = int((self.today_goal - self.final_goal) * 0.01)
        self.save()

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
        self.today_progress += progress
        if save:
            self.save()

        user: User = self.user
        user.is_recording = False
        user.save()

    def is_due_or_done(self):
        return self.is_today_due_date or self.today_progress > 0 or self.is_running

    def save_round_record_if_running(self):
        if self.is_running:
            round_record = RoundRecord()
            round_record.create_from_habit_running(self)
            self.add_progress_and_init(round_record.progress, save=False)

    def adjust_goal_and_due_date_by_success(self, success: bool):
        if self.growth_type == "INCREASE":
            growth_amount = self.growth_amount
        elif self.growth_type == "DECREASE":
            growth_amount = -self.growth_amount

        if success:
            self.today_goal += growth_amount
        else:
            self.today_goal -= growth_amount

        self.today_progress = 0

        # 예정일이 아니었는데 진행한 경우, 원래는 None이라 오류 남
        # => 어제로 예정일을 바꿈
        self.due_date = self.user.get_yesterday()
        self.due_date += timedelta(days=self.day_cycle)

    def set_is_today_due_date(self):
        if self.due_date == None:
            self.is_today_due_date = False

        user: User = self.user
        due_date_start = datetime.combine(self.due_date, user.daily_reset_time)
        due_date_end = due_date_start + timedelta(days=1)

        now = datetime.now()
        if now < due_date_start:
            self.is_today_due_date = False
        elif due_date_start <= now < due_date_end:
            self.is_today_due_date = True
        elif due_date_end <= now:
            # 원래 예정일에 접속했더라면 알아서 다음 날로 갱신이 됨.
            # 이 경우는 예정일에 아예 접속조차 안 해서 갱신이 안 됐던 상황.
            # 밀린 게 쌓였을 수 있으므로, 부담을 줄이기 위해 예정에서 빼놓기
            self.is_today_due_date = False

    def is_today_successful(self) -> bool:
        if self.growth_type == "INCREASE":
            return self.today_goal <= self.today_progress
        elif self.growth_type == "DECREASE":
            return self.today_goal >= self.today_progress

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
        self.goal = habit.today_goal
        self.progress = habit.today_goal
        self.excess = habit.today_progress

    def set_for_lack(self, habit: Habit):
        self.goal = habit.today_goal
        self.progress = habit.today_progress
        self.excess = 0

    def is_owned_by_user(self, given_user: User):
        return self.habit.is_owned_by_user(given_user)
