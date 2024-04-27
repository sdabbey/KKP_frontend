
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
import base64
from django.utils.encoding import smart_str
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from .utils import generate_qr_code, generate_receipt
# Create your views here.

@login_required(login_url="/login/")
def bookingpage(request):
    if request.method == 'POST':
        
        try:
            data = request.POST
            full_name = data.get('full_name')
            index_number = data.get('index_number')
            phone_number = data.get('phone_number')
            location = data.get('location')
            luggage_number = data.get('luggage_number')

            # Create a new Booking instance
            booking = Booking.objects.create(
                full_name=full_name,
                index_number=index_number,
                phone_number=phone_number,
                location=location,
                luggage_number=luggage_number
            )

            qrcode_image = generate_qr_code(booking.booking_code)
            # Since the booking code is generated automatically on save, you can access it after saving
            qr_code_base64 = base64.b64encode(qrcode_image.getvalue()).decode()
           
            context = {
                "booking": booking,
                "qrcode_image": qr_code_base64,

            }


            return render(request, "main/bookingsuccess.html", context)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    else:
        
        return render(request, "main/bookingpage.html")

@login_required(login_url="/login/")
def bookingsuccess(request):
    return render(request, "main/bookingsuccess.html")


def download_receipt(request, booking_code):
    receipt_pdf = generate_receipt(booking_code)
    if receipt_pdf:
        response = HttpResponse(receipt_pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{smart_str(booking_code)}.pdf"'
        return response
    else:
        return HttpResponse("Receipt not found", status=404)

#Work on this
@login_required(login_url="/login/")
def dashboard(request):
    bookings = Booking.objects.all()
    qrcode_images = []
    for booking in bookings:
        qrcode_image = generate_qr_code(booking.booking_code)
            # Since the booking code is generated automatically on save, you can access it after saving
        qrcode_images += base64.b64encode(qrcode_image.getvalue()).decode()
    context = {
        "bookings": bookings,
        "qrcode_images": qrcode_images
    }
    return render(request, "main/dashboard.html", context)

def delete_booking(request, booking_id):
    # Retrieve the booking object
    booking = get_object_or_404(Booking, pk=booking_id)

    if booking:
        # If the request method is POST, it means the user has confirmed the deletion
        booking.delete()
        return redirect('adminpage')

    # If the request method is not POST, render the confirmation template
    return HttpResponse("Booking not found", status=404)


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



