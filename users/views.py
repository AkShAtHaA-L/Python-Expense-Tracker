from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.models import User

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


#profile method, takes first name and second name from user and updates user-profile only if user is logged in
def profile(request):
    if request.user.is_authenticated:
        user_object = User.objects.get(pk=int(request.user.id))
        if request.method == "POST":
            updated_fname = request.POST.get("user-fname")
            updated_lname = request.POST.get("user-lname")
            user_object.first_name = updated_fname
            user_object.last_name = updated_lname
            user_object.save()
            messages.add_message(request, messages.INFO, f"{user_object} , your user-info updated")
        
        context = {
        'username' : user_object.username,
        'useremail': user_object.email,
        'userfname': user_object.first_name,
        'userlname': user_object.last_name
        }
        return render(request, "users/profile.html", context=context)
    
    else:
        messages.add_message(request, messages.INFO, f"please login to view user-profile")
        return redirect('login')