from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status

from .models import Habit


def authenticate_and_authorize(view):
    def wrapper(request: HttpRequest, habit_id=None):
        if request.method == "POST":
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

        if request.method != "POST":
            # Fixed from == 'GET' to != 'POST'
            # for including 'DELETE' method.
            return view(request, habit_id)
        else:
            return view(request)

    return wrapper
