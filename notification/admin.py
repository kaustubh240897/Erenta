from django.contrib import admin
from .models import Notification,Order_Notification,Supplier_Order_Notification,Order_current_status,User_Order_Status_Notification
from orders.models import Low_Quantity_Notification

# Register your models here.
admin.site.register(Notification)
admin.site.register(Order_Notification)
admin.site.register(Supplier_Order_Notification)
admin.site.register(Low_Quantity_Notification)
admin.site.register(Order_current_status)
admin.site.register(User_Order_Status_Notification)