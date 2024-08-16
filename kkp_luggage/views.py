from main.models import User
from django.shortcuts import render, redirect

def create_superuser(request):
    password = "testing321"
    if User.objects.filter(email='admin@kkp.com').exists():
        return redirect("bookingpage")
    User.objects.create_superuser(email='admin@kkp.com', password=password)
    user = User.objects.get(email='admin@kkp.com')
    user.set_password(password)
    user.save()
    return redirect("bookingpage")