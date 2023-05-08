
from django.contrib import admin
from django.urls import path,include,reverse_lazy
from . import views as user_views
from django.contrib.auth import views as authentication_views

urlpatterns = [
    path('', authentication_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path('register/', user_views.register, name="register"),
    path("login/",authentication_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/",authentication_views.LogoutView.as_view(next_page=reverse_lazy('login')),name="logout")
]
