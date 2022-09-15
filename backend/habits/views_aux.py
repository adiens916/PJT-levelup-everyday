import json
from typing import Iterable

from django.core import serializers
from django.db.models import Model
from django.http import JsonResponse


def json_response_wrapper(queryset: Iterable[Model]):
    queryset_json = serializers.serialize('json', queryset, ensure_ascii=False)
    queryset_dict = json.loads(queryset_json)
    return JsonResponse(queryset_dict, safe=False)

