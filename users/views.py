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
            messages.add_message(request, messages.INFO, f"{new_username} , your account is created, please login")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html',{'form':form})

def profile(request):
    if request.user.is_authenticated:
        print(request.POST)
        if request.method == "POST":
            updated_email = request.POST.get("user-email")
            user_object = User.objects.get(pk=int(request.user.id))
            user_object.email = updated_email
            user_object.save()
        
        username = request.user
        context = {
           'username' : username
        }
        return render(request, "users/profile.html", context=context)
    else:
        messages.add_message(request, messages.INFO, f"please login to view user-profile")
        return redirect('login')