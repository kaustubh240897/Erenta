from django.contrib import admin
from .models import Order,order_details
# Register your models here.

admin.site.register(Order)
admin.site.register(order_details)
