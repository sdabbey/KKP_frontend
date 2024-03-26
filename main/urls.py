from django.urls import path
from .views import *
urlpatterns = [
    path('', bookingpage, name="bookingpage"),
    path('adminpage/', adminpage, name="adminpage"),
    path('login/', loginpage, name="login"),
     path('success/', bookingsuccess, name="bookingsuccess"),
]
