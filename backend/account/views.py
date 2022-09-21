import datetime
import json

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import (
    authenticate,
    login as user_login, 
    logout as user_logout, 
)
from django.http import (
    JsonResponse, 
    HttpRequest, 
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

from .models import User


# Create your views here.
@csrf_exempt
@permission_classes([AllowAny])
def signup(request: HttpRequest):
    def create_user(request: HttpRequest) -> User:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username, email, password)
        return user

    def change_standard_reset_time(request: HttpRequest) -> None:
        standard_reset_time = request.POST.get('standard_reset_time')
        # ex) '03:30'
        # TODO: 정규표현식으로 체크하기
        if standard_reset_time:
            hour, minute = standard_reset_time.split(':')
            user.daily_reset_time = datetime.time(int(hour), int(minute))
            user.save()


    if request.method == 'POST':
        user = create_user(request)
        change_standard_reset_time(request)
        return JsonResponse({'id': user.pk})    
    else:
        return HttpResponseBadRequest()


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request: HttpRequest):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
        })
        user_login(request, user)
        return JsonResponse({
            'id': user.pk, 
            'name': user.get_username(),
            'last_login': user.last_login
        })
    else:
        result = json.dumps({'success': False, 'error': 'User not found'})
        return HttpResponseNotFound(result, content_type='application/json')


@csrf_exempt
@api_view(['POST'])
def logout(request: HttpRequest):
    if request.user.is_authenticated:
        request.user.auth_token.delete()
        return Response(
            {'success': True, 'detail': 'Successfully logged out'}, 
            status=status.HTTP_200_OK
        )
        user_logout(request)
        return JsonResponse({
            'success': True,
            'message': 'Successfully logged out'
        })
    else:
        result = json.dumps({'success': False, 'error': 'User not logged in'})
        return HttpResponseNotFound(result, content_type='application/json')


@csrf_exempt
def check_authenticated(request: HttpRequest):
    if not request.user:
        result = json.dumps({'success': False, 'error': 'User not found'})
        return HttpResponseNotFound(result, content_type='application/json')

    if request.user.is_authenticated:
        result = {
            'id': request.user.pk, 
            'name': request.user.get_username(),
            'post': request.POST,
            # 'meta': request.META,
            # 'headers': request.headers,
            # 'body': request.body,
            # 'session': list(request.session.values()),
        }
        return JsonResponse(result)

    else:
        result = json.dumps({'success': False, 'error': 'User not authenticated'})
        return HttpResponseNotFound(result, content_type='application/json')
