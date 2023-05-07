from django.contrib import admin
from django.urls import path,include
from . import views as transaction_views
from django.contrib.auth import views as authentication_views

urlpatterns = [
    path("", transaction_views.index, name="index_page")
]