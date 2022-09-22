from datetime import date, timedelta
from django.http import (
    JsonResponse,
    HttpRequest, 
    HttpResponse,
)
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from account.models import User
from .models import Habit, RoundRecord
from .views_aux import (
    json_response_wrapper,
    is_day_changed_for_user,
    update_goals_and_due_dates
) 


# Create your views here.
@csrf_exempt
@api_view(['GET', 'POST'])
def index(request: HttpRequest):
    if not request.user.is_authenticated:
        result = {'success': False, 'error': 'User not authenticated'}
        return Response(result, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        user: User = request.user
        habit_list = Habit.objects.filter(user=user.pk)
        if is_day_changed_for_user(user):
            print('day changed')
            if user.next_reset_date:
                # TODO: 자정 후에 미리 다음 날로 넘어가는 기능 추가하기
                update_goals_and_due_dates(habit_list)
            user.next_reset_date = date.today() + timedelta(days=1)
            user.save()
        return json_response_wrapper(habit_list)
    
    elif request.method == 'POST':
        habit = Habit()
        
        habit.user = request.user
        habit.name = request.POST.get('name')
        habit.estimate_type = request.POST.get('estimate_type')
        habit.estimate_unit = request.POST.get('estimate_unit')
        habit.final_goal = int(request.POST.get('final_goal'))
        habit.growth_type = request.POST.get('growth_type')
        habit.day_cycle = int(request.POST.get('day_cycle'))

        # 임시로 초기 목표 & 증감량 설정
        habit.today_goal = int(habit.final_goal * 0.01)
        habit.growth_amount = int(habit.final_goal * 0.01)
        
        habit.save()
        return JsonResponse({'id': habit.pk})


@csrf_exempt
@api_view(['GET'])
def index_each(request: HttpRequest, habit_id: int):
    if not request.user.is_authenticated:
        return Response({
            'success': False, 
            'error': 'User not authenticated'
        }, status=status.HTTP_401_UNAUTHORIZED)
        
    user: User = request.user
    habit = Habit.objects.filter(user=user.pk, pk=habit_id)

    if len(habit) and user.pk == habit[0].user.pk:
        return json_response_wrapper(habit)
    else:
        return Response({
            'success': False,
            'detail': "Habit not owned by the user"
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['POST'])
def start_timer(request: HttpRequest):
    if request.method == 'POST':
        habit_id = request.POST.get('habit_id')
        habit: Habit = Habit.objects.get(id=habit_id)

        habit.start_datetime = timezone.now()
        habit.is_running = True
        habit.save()

        user: User = habit.user
        user.is_recording = True
        user.save()

        return JsonResponse({
            'success': True, 
            'start_date': habit.start_datetime,
            'is_running': habit.is_running
        })
    else:
        return JsonResponse({
            'success': False,
            'error': 'POST method only allowed'
        })


@csrf_exempt
@api_view(['POST'])
def finish_timer(request: HttpRequest):
    if request.method == 'POST':
        habit_id = request.POST.get('habit_id')
        habit: Habit = Habit.objects.get(id=habit_id)

        record = RoundRecord()
        record.habit = habit
        record.start_datetime = habit.start_datetime
        record.end_datetime = timezone.now()
        record.progress = int(request.POST.get('progress'))
        record.save()

        habit.start_datetime = None
        habit.is_running = False
        habit.today_progress += record.progress
        habit.save()

        user: User = habit.user
        user.is_recording = False
        user.save()

        return json_response_wrapper([record])
        # return JsonResponse({
        #     'success': True,
        #     'start_date': habit.start_date,
        #     'is_running': habit.is_running
        # })
