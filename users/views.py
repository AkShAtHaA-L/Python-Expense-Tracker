from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import RegisterForm

# Create your views here.

#register view that uses RegisterForm class, to save the user only if the form is valid.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Welcome {username}")
            return redirect('user-login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html',{'form':form})

