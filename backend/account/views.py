from datetime import date, timedelta
import json

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.http import (
    JsonResponse,
    HttpRequest,
    HttpResponseNotFound,
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .models import User


# Create your views here.
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request: HttpRequest):
    user = User.create_from_request(request)
    user.change_standard_reset_time(request)
    user.next_reset_date = date.today() + timedelta(days=1)
    user.save()
    return JsonResponse({"id": user.pk})


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request: Request):
    # print("data", request.data)
    # print("POST", request.POST)

    if len(request.data) == 0:
        return Response(
            {"success": False, "error": "No data in request"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
            }
        )
    else:
        result = json.dumps({"success": False, "error": "User not found"})
        return HttpResponseNotFound(result, content_type="application/json")


@csrf_exempt
@api_view(["POST"])
def logout(request: HttpRequest):
    if request.user.is_authenticated:
        request.user.auth_token.delete()
        return Response(
            {"success": True, "detail": "Successfully logged out"},
            status=status.HTTP_200_OK,
        )
    else:
        result = json.dumps({"success": False, "error": "User not logged in"})
        return HttpResponseNotFound(result, content_type="application/json")


@csrf_exempt
@api_view(["GET"])
@permission_classes([AllowAny])
def check_connection(request: HttpRequest):
    return Response("connected")


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def check_post_availability(request: HttpRequest):
    return Response("post available")


@csrf_exempt
@api_view(["POST"])
def check_authenticated(request: HttpRequest):
    if not request.user:
        result = json.dumps({"success": False, "error": "User not found"})
        return HttpResponseNotFound(result, content_type="application/json")

    if request.user.is_authenticated:
        result = {
            "id": request.user.pk,
            "name": request.user.get_username(),
            "post": request.POST,
        }
        return JsonResponse(result)

    else:
        result = json.dumps({"success": False, "error": "User not authenticated"})
        return HttpResponseNotFound(result, content_type="application/json")
