from django.shortcuts import render,redirect
from django.contrib import messages

# Create your views here.


def dashboard(request):
    return render(request, "transactions/index.html")

def newentry(request):
    return render(request, "transactions/newtransaction.html")
