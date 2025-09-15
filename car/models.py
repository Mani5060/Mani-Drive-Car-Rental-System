from django.db import models 
from django.contrib.auth.models import User
from django.utils import timezone


class Contact(models.Model):
    name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    city = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Cars(models.Model):
    CATEGORY_CHOICES = [
        ('hatchback', 'Hatchback'),
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('van', 'Van / Minivan'),
        ('luxury', 'Luxury'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]
    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    ]
    FUEL_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('cng', 'CNG'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]

    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES)
    transmission = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES)
    seats = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)
    cimage = models.ImageField(upload_to='image')
    location = models.CharField(max_length=100, default='Pune')
    description = models.TextField(default="Car description")

    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    car = models.ForeignKey(Cars, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, blank=True)
    pickup_datetime = models.DateTimeField(default=timezone.now)
    drop_datetime = models.DateTimeField(default=timezone.now)
    customer_name = models.CharField(max_length=100, null=True, blank=True)
    license_no = models.CharField(max_length=100, default="N/A")
    no_of_days = models.PositiveIntegerField(default=1)
    address = models.CharField(max_length=200, default="N/A")
    pickup_location = models.CharField(max_length=100, blank=True)
    mobile = models.CharField(max_length=10, default="N/A")
    license_file = models.FileField(upload_to='licenses/', blank=True, null=True)
    addhar_file = models.FileField(upload_to='addhar/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_paid=models.BooleanField(default=False)

    def __str__(self):
        return f"Booking by {self.customer_name} for {self.car.name}"
