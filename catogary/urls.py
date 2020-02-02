from django.contrib import admin
from django.urls import path
from .views import catogary_product_view



urlpatterns = [
   
    path('<slug:slug>/',catogary_product_view , name='query'),
    

    
]

