from django.urls import path
from . import views

urlpatterns = [
    path("accounts/", views.register_user, name="register"),
    path("accounts/login", views.login_user, name="login"),
]
