from django.contrib import admin
from django.urls import path
from .views import category_product_view



urlpatterns = [
   
    path('<slug:slug>/',category_product_view , name='query'),
    

    
]

