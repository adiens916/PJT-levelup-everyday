from rest_framework import serializers
from .models import *


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"


class RoundRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoundRecord
        fields = "__all__"


class DailyRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyRecord
        fields = "__all__"
