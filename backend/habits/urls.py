from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("<int:habit_id>/", views.index_each),
    path("<int:habit_id>/importance", views.update_importance),
    path("<int:habit_id>/record/", views.get_daily_records),
    path("timer/start/", views.start_timer),
    path("timer/finish/", views.finish_timer),
]
