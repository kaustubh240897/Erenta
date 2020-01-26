from django.contrib import admin
from django.urls import path
from .views import OrderListView, OrderDetailView,SupplierOrdersListView,SupplierOrderDetailView,AddCouponView


urlpatterns = [
   
    path('', OrderListView.as_view(), name='list'),
    path('<order_id>[0-9A-Za-z]+/', OrderDetailView.as_view(), name='detail'),
    path('orders/',SupplierOrdersListView.as_view(),name='orders'),
    path('orders/<order_id>[0-9A-Za-z]+/', SupplierOrderDetailView.as_view(), name='supplierorderdetail'),
    path('add_coupon/',AddCouponView.as_view(),name='add-coupon')

    
   
]

