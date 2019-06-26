from django.contrib import admin
from django.urls import path
from .views import OrderListView, OrderDetailView


urlpatterns = [
   
    path('', OrderListView.as_view(), name='list'),
    path('(<order_id>[0-9A-Za-z]+)/', OrderDetailView.as_view(), name='detail'),
    
   
]

