from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

# from drf_yasg.utils import swagger_auto_schema

from account.models import User
from .models import Habit, RoundRecord, DailyRecord
from .models_aux import RecordSaver, GoalAdjuster, DueAdjuster
from .serializers import HabitSerializer, RoundRecordSerializer, DailyRecordSerializer
from .views_aux import authenticate_and_authorize

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
            for habit in habit_list:
                RecordSaver.save(habit)
                GoalAdjuster.adjust_habit_goal(habit)
                DueAdjuster.adjust_habit_due(habit)
                DueAdjuster.set_is_today_due_date(habit)
                habit.save()

        serializer = HabitSerializer(habit_list, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        habit = Habit()
        habit.create_from_request(request)
        # Instead of DRF Response, you can use Django's built-in JsonResponse
        return JsonResponse({"id": habit.pk})


@csrf_exempt
@api_view(["GET", "DELETE"])
@authenticate_and_authorize
def index_each(request: HttpRequest, habit_id: int):
    habit = get_object_or_404(Habit, pk=habit_id)

    if request.method == "GET":
        serializer = HabitSerializer(habit)
        return Response(serializer.data)

    elif request.method == "DELETE":
        habit.delete()
        return Response(
            {"success": True, "detail": "the habit's successfully deleted"},
        )


@csrf_exempt
@api_view(["PATCH"])
@authenticate_and_authorize
def update_importance(request: Request, habit_id: int):
    habit = get_object_or_404(Habit, pk=habit_id)

    habit.importance = request.data.get("importance")
    habit.save()
    return Response(
        {"success": True, "detail": "Updated successfully"},
        status=status.HTTP_200_OK,
    )


@csrf_exempt
@api_view(["GET"])
@authenticate_and_authorize
def get_daily_records(request: HttpRequest, habit_id: int):
    records = DailyRecord.objects.filter(habit=habit_id)
    serializer = DailyRecordSerializer(records, many=True)
    return Response(serializer.data)


@csrf_exempt
@api_view(["POST"])
@authenticate_and_authorize
def start_timer(request: Request):
    habit_id = request.data.get("habit_id")
    habit = Habit.objects.get(id=habit_id)

    habit.start_recording()
    return Response(
        {
            "success": True,
            "start_date": habit.start_datetime,
            "is_running": habit.is_running,
        }
    )


@csrf_exempt
@api_view(["POST"])
@authenticate_and_authorize
def finish_timer(request: Request):
    habit_id = request.data.get("habit_id")
    habit: Habit = Habit.objects.get(id=habit_id)
    progress = int(request.data.get("progress"))

    record = RoundRecord()
    record.create_from_habit_finished(habit, progress)
    habit.end_recording(record.progress)

    serializer = RoundRecordSerializer(record)
    return Response(serializer.data)
