from django.contrib import admin
from django.urls import path,include
from . import views as transaction_views
from django.contrib.auth import views as authentication_views

urlpatterns = [
    path("", transaction_views.dashboard, name="dashboard"),
    path("transaction/", transaction_views.newentry, name="newtransaction"),
    path("allexpenses/",transaction_views.allentries,name="allexpenses"),
    path("edit/<int:id>",transaction_views.edit_entry,name="edit"),
    path("delete/<int:id>",transaction_views.delete_entry,name="delete")
]