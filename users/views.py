from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from .models import UserProfile

# Create your views here.

#register view that uses RegisterForm class, to save the user only if the form is valid.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            new_username = form.cleaned_data.get("username")
            #new_user = User.objects.get(username=new_username)
            #UserProfile.objects.create(new_user,20000)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html',{'form':form})

def profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            print(request.POST.get("user-budget"))
        username = request.user
        budget_of_user = UserProfile.objects.get(user=username).monthly_budget
        context = {
           'username' : username,
           'budget_of_user': budget_of_user
        }
        return render(request, "users/profile.html", context=context)
    else:
        return redirect('login')