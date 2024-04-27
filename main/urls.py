from django.urls import path
from .views import *
urlpatterns = [
    path('', bookingpage, name="bookingpage"),
    path('dashboard/', adminpage, name="adminpage"),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),
    path('success/', bookingsuccess, name="bookingsuccess"),
    path('success/download_receipt/<str:booking_code>/', download_receipt, name="download_receipt"),
]
