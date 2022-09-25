from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("<int:habit_id>/", views.index_each),
    path("timer/start/", views.start_timer),
    path("timer/finish/", views.finish_timer),
    path("record/<int:habit_id>/", views.get_daily_records),
]
