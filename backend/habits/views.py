from typing import Iterable

from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from account.models import User
from .models import DailyRecord, Habit, RoundRecord
from .models_aux import RecordSaver, GoalAdjuster, DueAdjuster
from .views_aux import json_response_wrapper


# Create your views here.
@csrf_exempt
@api_view(["GET", "POST"])
def index(request: HttpRequest):
    if not request.user.is_authenticated:
        result = {"success": False, "error": "User not authenticated"}
        return Response(result, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        user: User = request.user
        habit_list = Habit.objects.filter(user=user.pk).order_by("-importance")
        if user.is_day_changed():
            # TODO: 자정 후에 미리 다음 날로 넘어가는 기능 추가하기
            for habit in habit_list:
                RecordSaver.save(habit)
                GoalAdjuster.adjust_habit_goal(habit)
                DueAdjuster.adjust_habit_due(habit)
                DueAdjuster.set_is_today_due_date(habit)
                habit.save()

        return json_response_wrapper(habit_list)

    elif request.method == "POST":
        habit = Habit()
        habit.create_from_request(request)
        return JsonResponse({"id": habit.pk})


@csrf_exempt
@api_view(["GET", "POST"])
def index_each(request: HttpRequest, habit_id: int):
    if not request.user.is_authenticated:
        return Response(
            {"success": False, "error": "User not authenticated"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if request.method == "GET":
        user: User = request.user
        habit = Habit.objects.filter(user=user.pk, pk=habit_id)

        if len(habit) and user.pk == habit[0].user.pk:
            return json_response_wrapper(habit)
        else:
            return Response(
                {"success": False, "detail": "Habit not owned by the user"},
                status=status.HTTP_404_NOT_FOUND,
            )

    else:  # request.method == 'DELETE
        habit = Habit.objects.get(pk=habit_id)
        if not habit.is_owned_by_user(request.user):
            return Response(
                {"success": False, "detail": "Habit not owned by the user"},
                status=status.HTTP_404_NOT_FOUND,
            )

        habit.delete()
        return Response(
            {"success": True, "detail": "the habit's successfully deleted"},
            status=status.HTTP_200_OK,
        )


@csrf_exempt
@api_view(["POST"])
def update_importance(request: HttpRequest, habit_id: int):
    if not request.user.is_authenticated:
        return Response(
            {"success": False, "detail": "User not authenticated"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    habit = Habit.objects.get(pk=habit_id)
    if not habit.is_owned_by_user(request.user):
        return Response(
            {"success": False, "detail": "Habit not owned by the user"},
            status=status.HTTP_404_NOT_FOUND,
        )

    habit.importance = request.POST.get("importance")
    habit.save()
    return Response(
        {"success": True, "detail": "Updated successfully"},
        status=status.HTTP_200_OK,
    )


@csrf_exempt
@api_view(["GET"])
def get_daily_records(request: HttpRequest, habit_id: int):
    if not request.user.is_authenticated:
        return Response(
            {"success": False, "detail": "User not authenticated"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    records: Iterable[DailyRecord] = DailyRecord.objects.filter(habit=habit_id)

    user: User = request.user
    if len(records) and records[0].is_owned_by_user(user):
        return json_response_wrapper(records)
    # 아직 기록이 없을 때
    elif len(records) == 0:
        return json_response_wrapper([])
    else:
        return Response(
            {"success": False, "detail": "Not owned by user"},
            status=status.HTTP_404_NOT_FOUND,
        )


@csrf_exempt
@api_view(["POST"])
def start_timer(request: HttpRequest):
    habit_id = request.POST.get("habit_id")
    habit = Habit.objects.get(id=habit_id)
    habit.save_start_datetime()
    return JsonResponse(
        {
            "success": True,
            "start_date": habit.start_datetime,
            "is_running": habit.is_running,
        }
    )


@csrf_exempt
@api_view(["POST"])
def finish_timer(request: HttpRequest):
    habit_id = request.POST.get("habit_id")
    habit: Habit = Habit.objects.get(id=habit_id)
    progress = int(request.POST.get("progress"))

    record = RoundRecord()
    record.create_from_habit_finished(habit, progress)
    habit.add_progress_and_init(record.progress)

    return json_response_wrapper([record])
