import json
from typing import Iterable

from django.core import serializers
from django.db.models import Model
from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from .models import Habit


def json_response_wrapper(queryset: Iterable[Model]):
    queryset_json = serializers.serialize("json", queryset, ensure_ascii=False)
    queryset_dict = json.loads(queryset_json)
    return JsonResponse(queryset_dict, safe=False)


def authenticate_and_authorize(view):
    def wrapper(request: HttpRequest, *args):
        if any(args):
            habit_id = args[0]
        else:
            habit_id = request.POST.get("habit_id")

        if not request.user.is_authenticated:
            return Response(
                {"success": False, "detail": "User not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        habit = get_object_or_404(Habit, pk=habit_id)
        if not habit.is_owned_by_user(request.user):
            return Response(
                {"success": False, "detail": "Not owned by user"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if any(args):
            return view(request, habit_id)
        else:
            return view(request)

    return wrapper
