from django.contrib import admin
from django.urls import path
from .views import cart_home,checkout_home,checkout_done_view,add_to_cart,remove_cart


urlpatterns = [
   
    path('',cart_home, name='home'),
    #path('<slug:slug>/',update_cart, name='update_cart'),
    path('remove/<int:id>/', remove_cart, name='remove_cart'),
    path('<int:id>/', add_to_cart, name='add_to_cart'),
    path('checkout/success/', checkout_done_view, name='success'),
    path('checkout/', checkout_home, name='checkout')
]

