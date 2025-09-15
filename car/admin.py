from django.contrib import admin
from car.models import Cars,Booking
# Register your models here.

class CarAdmin(admin.ModelAdmin):
    list_display=['id','name','price','brand','category','fuel_type','transmission','seats','available','cimage']

class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'car', 'pickup_datetime', 'drop_datetime', 'customer_name', 'created_at']

admin.site.register(Cars,CarAdmin)
admin.site.register(Booking,BookingAdmin)