from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('timer/start/', views.start_timer),
    path('timer/finish/', views.finish_timer),
]
