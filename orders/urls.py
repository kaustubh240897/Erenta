from django.contrib import admin
from django.urls import path
from .views import OrderListView, OrderDetailView,SupplierOrdersListView,SupplierOrderDetailView,AddCouponView,CreatedOrderDetailView,CreatedOrderView,created_order_checkout_home,shipping_address_update_view,billing_address_update_view

urlpatterns = [
   
    path('', OrderListView.as_view(), name='list'),
    path('<order_id>[0-9A-Za-z]+/', OrderDetailView.as_view(), name='detail'),
    path('created/', CreatedOrderView.as_view(), name='created'),
    path('created/<order_id>/', CreatedOrderDetailView.as_view(), name='createddetail'),
    path('orders/',SupplierOrdersListView.as_view(),name='orders'),
    path('orders/<order_id>[0-9A-Za-z]+/', SupplierOrderDetailView.as_view(), name='supplierorderdetail'),
    path('add_coupon/',AddCouponView.as_view(),name='add-coupon'),
    path('created_orders/<order_id>/',created_order_checkout_home,name='created_orders'),
    path('update_address/<order_id>/',shipping_address_update_view,name='update_address'),
    path('update_billingaddress/<order_id>/',billing_address_update_view,name='update_billingaddress'),
    


    
   
]

