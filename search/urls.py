from django.contrib import admin
from django.urls import path
from .views import search_product_view


urlpatterns = [
   
    path('',search_product_view , name='query'),
    
]

