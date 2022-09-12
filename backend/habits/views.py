import json
from typing import Iterable

from django.core import serializers
from django.db.models import Model
from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .models import Habit


def json_response_wrapper(queryset: Iterable[Model]):
    queryset_json = serializers.serialize('json', queryset, ensure_ascii=False)
    queryset_dict = json.loads(queryset_json)
    return JsonResponse(queryset_dict, safe=False)


# Create your views here.
@csrf_exempt
def index(request: HttpRequest):
    if request.method == 'GET':
        habit_list = Habit.objects.all()
        return json_response_wrapper(habit_list)
    
    elif request.method == 'POST':
        habit = Habit()
        
        habit.name = request.POST.get('name')
        habit.estimate_type = request.POST.get('estimate_type')
        habit.estimate_unit = request.POST.get('estimate_unit')
        habit.final_goal = int(request.POST.get('final_goal'))
        habit.growth_type = request.POST.get('growth_type')
        habit.day_cycle = int(request.POST.get('day_cycle'))
        
        habit.save()
        return JsonResponse({'id': habit.pk})


@csrf_exempt
def start_timer(request: HttpRequest, habit_id: int):
    if request.method == 'POST':
        habit: Habit = Habit.objects.get(id=habit_id)

        habit.start_date = timezone.now()
        habit.is_running = True
        habit.save()

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
