
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
import base64
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
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
    qrcode_data = []

    for booking in bookings:
        qrcode_image = generate_qr_code(booking.booking_code)
        if qrcode_image:
            # Convert the QR code image to a base64 string
            qrcode_base64 = base64.b64encode(qrcode_image.getvalue()).decode()
            qrcode_data.append({'booking': booking, 'qrcode': qrcode_base64})
        else:
            # If QR code generation fails, append None
            qrcode_data.append({'booking': booking, 'qrcode': None})

    context = {
        "qrcode_data": qrcode_data
    }
    print(qrcode_data)
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

def search_bookings(request):
    search_query = request.GET.get('searchbox', '')
    if search_query:
        # Perform case-insensitive search by name or full name
        bookings = Booking.objects.filter(full_name__icontains=search_query) | \
                   Booking.objects.filter(booking_code__icontains=search_query)
    else:
        bookings = Booking.objects.all()

    search_results = []
    for booking in bookings:
        # Generate QR code for each booking
        qr_code_image = generate_qr_code(booking.booking_code)
        if qr_code_image:
            # Convert the QR code image to a base64 string
            qr_code_base64 = base64.b64encode(qr_code_image.getvalue()).decode()
        else:
            qr_code_base64 = None
        
        # Append booking and QR code data to search results
        search_results.append({'booking': booking, 'qr_code': qr_code_base64})

    context = {
        'search_results': search_results,
        'search_query': search_query
    }

    return render(request, 'main/dashboard.html', context)

def download_all_bookings(request):
    bookings = Booking.objects.all()

    # Create a PDF canvas
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Add title to the PDF
    c.drawString(100, 760, 'All Bookings')

    # Add booking details to the PDF
    y_offset = 680
    for booking in bookings:
        # Generate QR code for each booking
        qr_code_image = generate_qr_code(booking.booking_code)
        if qr_code_image:
            # Convert the QR code image to a base64 string
            qr_code_base64 = base64.b64encode(qr_code_image.getvalue()).decode()
            qr_code_image_reader = ImageReader(qr_code_image)
            c.drawImage(qr_code_image_reader, 100, y_offset - 50, width=100, height=100)
        else:
            qr_code_base64 = None
        
        c.drawString(220, y_offset + 20, f'Booking Code: {booking.booking_code}')
        c.drawString(220, y_offset, f'Name: {booking.full_name}')
        c.drawString(220, y_offset - 20, f"Phone Number: {booking.phone_number}")
        c.drawString(220, y_offset - 40, f'Luggage Number: {booking.luggage_number}')

        # Increase y_offset for the next booking
        y_offset -= 130

    # Save the PDF
    c.showPage()
    c.save()

    # Set response content type and headers for file download
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="all_bookings.pdf"'
    return response

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



