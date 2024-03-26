from django.shortcuts import render

# Create your views here.

def bookingpage(request):
    return render(request, "main/bookingpage.html")


def bookingsuccess(request):
    return render(request, "main/bookingsuccess.html")

def adminpage(request):
    return render(request, "main/admin.html")