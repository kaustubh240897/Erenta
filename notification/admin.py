from django.contrib import admin
from .models import Notification,Order_Notification,Supplier_Order_Notification

# Register your models here.
admin.site.register(Notification)
admin.site.register(Order_Notification)
admin.site.register(Supplier_Order_Notification)