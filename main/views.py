from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
# Create your views here.

@login_required(login_url="/login/")
def bookingpage(request):
    return render(request, "main/bookingpage.html")


def bookingsuccess(request):
    return render(request, "main/bookingsuccess.html")

def adminpage(request):
    return render(request, "main/admin.html")




def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            
            return redirect("bookingpage")
        else:
            messages.error(request, "Username Or Password is incorrect!!",
                           extra_tags='alert alert-warning alert-dismissible fade show')
    return render(request, "main/login.html")

def logout_user(request):
    logout(request)
    return redirect('login')