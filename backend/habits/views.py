import json
from typing import Iterable

from django.core import serializers
from django.db.models import Model
from django.http import (
    JsonResponse,
    HttpRequest, 
    HttpResponseNotAllowed,
)
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from account.models import User
from .models import Habit, RoundRecord


def json_response_wrapper(queryset: Iterable[Model]):
    queryset_json = serializers.serialize('json', queryset, ensure_ascii=False)
    queryset_dict = json.loads(queryset_json)
    return JsonResponse(queryset_dict, safe=False)


# Create your views here.
@csrf_exempt
def index(request: HttpRequest):
    if not request.user.is_authenticated:
        result = {'success': False, 'error': 'User not authenticated'}
        return HttpResponseNotAllowed(result, content_type='application/json')

    if request.method == 'GET':
        habit_list = Habit.objects.filter(user=request.user.pk)
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
        
        habit.save()
        return JsonResponse({'id': habit.pk})


@csrf_exempt
def start_timer(request: HttpRequest):
    if request.method == 'POST':
        habit_id = request.POST.get('habit_id')
        habit: Habit = Habit.objects.get(id=habit_id)

        habit.start_date = timezone.now()
        habit.is_running = True
        habit.save()

        user: User = habit.user
        user.is_recording = True
        user.save()

        return JsonResponse({
            'success': True, 
            'start_date': habit.start_date,
            'is_running': habit.is_running
        })
    else:
        return JsonResponse({
            'success': False,
            'error': 'POST method only allowed'
        })


@csrf_exempt
def finish_timer(request: HttpRequest):
    if request.method == 'POST':
        habit_id = request.POST.get('habit_id')
        habit: Habit = Habit.objects.get(id=habit_id)

        record = RoundRecord()
        record.habit = habit
        record.start_date = habit.start_date
        record.end_date = timezone.now()
        record.progress = int(request.POST.get('progress'))
        record.save()

        habit.start_date = None
        habit.is_running = False
        habit.today_progress += record.progress
        habit.last_done_date = timezone.now()
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
