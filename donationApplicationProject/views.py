from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib import messages


# Create your views here.

def authentication_one(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User registered successfully, click on "Go back to Login" to Login')

            return redirect('authorise-url')
    else:
        form = RegistrationForm()
    return render(request, 'auth/authorise.html', {"form": form})


def home(request):
    return render(request, 'home.html')
# def register(request):
#   if request.method == "POST":
#      form = LoginForm(request.POST)
#   if form.is_valid():
#       form.save()
#       messages.success(request, 'User registered successfully')
#       return redirect('authorise-url')
# lse:
#    form = RegistrationForm()
# return render(request, 'auth/authentication.html', {"form": form})

