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
from .serializers import HabitSerializer, RoundRecordSerializer, DailyRecordSerializer
from .views_aux import authenticate, authenticate_and_authorize

# Create your views here.
@csrf_exempt
@api_view(["GET", "POST"])
@authenticate
def index(request: HttpRequest):
    if request.method == "GET":
        user: User = request.user
        habit_list = Habit.objects.filter(user=user.pk).order_by("-importance")
        __check_day_changes_and_update_habits(user, habit_list)

        serializer = HabitSerializer(habit_list, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        habit = Habit()
        habit.create_from_request(request)
        DailyRecord().create_from_habit(habit)

        # Instead of DRF Response, you can use Django's built-in JsonResponse
        return JsonResponse({"id": habit.pk})


def __check_day_changes_and_update_habits(user: User, habits: list[Habit]):
    if user.is_day_changed():
        for habit in habits:
            if habit.is_today_due_date and not habit.is_done:
                habit.lose_xp()
                DailyRecord.create_or_update_from_habit(habit)

            habit.update_due()
            habit.save()

            # daily record must be created for due habits only
            if habit.is_today_due_date:
                DailyRecord().create_from_habit(habit, is_for_new_day=True)

        # user's next reset date must be updated
        user.update_reset_date()


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
    user: User = habit.user

    record = RoundRecord()
    record.create_from_habit_finished(habit, progress)
    habit.end_recording(progress)

    DailyRecord.create_or_update_from_habit(habit)

    serializer = RoundRecordSerializer(record)
    return Response(serializer.data)
