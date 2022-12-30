from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup),
    path("login/", views.login),
    path("logout/", views.logout),
    path("check-conn/", views.check_connection),
    path("check-post/", views.check_post_availability),
    path("check-auth/", views.check_authenticated),
]
