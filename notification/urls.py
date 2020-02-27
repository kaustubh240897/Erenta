from django.urls import path
from django.contrib import admin
from .views import show_notification,delete_notification,show_order_notification,delete_order_notification,supplier_order_notification,delete_supplier_order_notification,low_quantity_supplier_notification,delete_supplier_lowquantity_notification
urlpatterns = [

   path('show/<int:notification_id>', show_notification, name='show_notification'),
   path('delete/<int:notification_id>', delete_notification, name='delete_notification'),
   path('order_show/<int:notification_id>', show_order_notification, name='show_order_notification'),
   path('delete_notification/<int:notification_id>', delete_order_notification, name='delete_order_notification'),
   path('supplier_order_show/<int:notification_id>', supplier_order_notification, name='supplier_order_notification'),
   path('delete_supplier_notification/<int:notification_id>', delete_supplier_order_notification, name='delete_supplier_order_notification'),
   path('low_quantity_show/<int:notification_id>', low_quantity_supplier_notification, name='supplier_quantity_notification'),
   path('delete_quantity_notification/<int:notification_id>', delete_supplier_lowquantity_notification, name='delete_supplier_quantity_notification'),


]
