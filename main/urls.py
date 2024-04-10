from django.urls import path
from .views import *
urlpatterns = [
    path('', bookingpage, name="bookingpage"),
    path('dashboard/', adminpage, name="adminpage"),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),
     path('success/', bookingsuccess, name="bookingsuccess"),
]
