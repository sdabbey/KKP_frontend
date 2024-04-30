import random, string
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    

class Booking(models.Model):
    full_name = models.CharField(max_length=200)
    amount = models.IntegerField()
    phone_number = PhoneNumberField(null=False, blank=False)
    opt_phone_number = PhoneNumberField(null=True, blank=True)
    location = models.CharField(max_length=150)
    luggage_number = models.IntegerField()
    booking_code = models.CharField(max_length=50, unique=True)
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Booking {self.pk}'
    
    @staticmethod
    def generate_booking_code(full_name, phone_number):
        # Concatenate parts of full_name and phone_number to generate a base code
        base_code = full_name[:3].upper() + str(phone_number)[-4:]

        # Generate a random suffix to ensure uniqueness
        suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        # Concatenate base_code and suffix to get the final booking code
        booking_code = base_code + suffix

        # Check if the generated code already exists in the database
        while Booking.objects.filter(booking_code=booking_code).exists():
            # If it does, generate a new suffix and try again
            suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            booking_code = base_code + suffix

        return booking_code

    def save(self, *args, **kwargs):
        # Generate a unique booking code before saving the object
        if not self.booking_code:
            self.booking_code = self.generate_booking_code(self.full_name, self.phone_number)
        super().save(*args, **kwargs)