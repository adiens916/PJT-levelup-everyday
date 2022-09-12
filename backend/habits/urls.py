from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('timer/start/<int:habit_id>/', views.start_timer),
    path('timer/finish/<int:habit_id>/', views.finish_timer),
]
