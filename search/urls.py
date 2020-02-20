from django.contrib import admin
from django.urls import path
from .views import search_product_view,search_product_view_for_supplier


urlpatterns = [
   
    path('',search_product_view , name='query'),
    path('supplier/',search_product_view_for_supplier,name='supplierquery'),
    
]

