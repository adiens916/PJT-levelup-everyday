from django.contrib import admin
from .models import Habit, RoundRecord, DailyRecord

# Register your models here.
admin.site.register(Habit)
admin.site.register(RoundRecord)
admin.site.register(DailyRecord)