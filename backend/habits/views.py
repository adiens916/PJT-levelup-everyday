import json
from typing import Iterable

from django.core import serializers
from django.db.models import Model
from django.http import HttpRequest, JsonResponse

from .models import Habit


def json_response_wrapper(queryset: Iterable[Model]):
    queryset_json = serializers.serialize('json', queryset, ensure_ascii=False)
    queryset_dict = json.loads(queryset_json)
    return JsonResponse(queryset_dict, safe=False)


# Create your views here.
def index(request: HttpRequest):
    if request.method == 'GET':
        habit_list = Habit.objects.all()
        return json_response_wrapper(habit_list)