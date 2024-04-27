from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import base64
from io import BytesIO
import requests
from .models import Booking

def generate_qr_code(booking_code):
    try:
        # Retrieve the booking object using the booking code
        booking = Booking.objects.get(booking_code=booking_code)

        # API endpoint for generating QR code
        api_url = f"https://api.qrserver.com/v1/create-qr-code/?data={booking_code}&size=200x200"

        # Make a GET request to the API
        response = requests.get(api_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Create an in-memory BytesIO object to store the QR code image
            buffer = BytesIO(response.content)
            buffer.seek(0)

            # Return the BytesIO object containing the QR code image
            return buffer
        else:
            return None
    except Booking.DoesNotExist:
        return None
    

def generate_receipt(booking_code):
    try:
        # Retrieve the booking object using the booking code
        booking = Booking.objects.get(booking_code=booking_code)

        # Generate QR code image BytesIO object
        qr_code_image = generate_qr_code(booking_code)

        if qr_code_image:
            # Create a PDF canvas
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)

            # Add booking details to the PDF
            c.drawString(220, 700, f"Booking Code: {booking.booking_code}")
            c.drawString(220, 680, f"Name: {booking.full_name}")
            c.drawString(220, 660, f"Phone Number: {booking.phone_number}")
            c.drawString(220, 640, f"Luggage Quantity: {booking.luggage_number}")

            # Embed QR code image into the PDF
            qr_code_image_reader = ImageReader(qr_code_image)
            c.drawImage(qr_code_image_reader, 100, 620, width=100, height=100)

            # Save the PDF
            c.showPage()
            c.save()

            # Return the PDF buffer
            buffer.seek(0)
            return buffer.getvalue()
        else:
            return None
    except Booking.DoesNotExist:
        return None