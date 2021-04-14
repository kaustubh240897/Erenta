from django.contrib import admin
from django.urls import path
from .views import cart_home,checkout_home,checkout_done_view,add_to_cart,remove_cart,remove_all_items,payment_method_default_update_view,remove_coupon_view


urlpatterns = [
   
    path('',cart_home, name='home'),
    #path('<slug:slug>/',update_cart, name='update_cart'),
    path('remove/<int:id>/', remove_cart, name='remove_cart'),
    path('removeall/', remove_all_items, name='remove_all'),
    path('<int:id>/', add_to_cart, name='add_to_cart'),
    path('checkout/success/', checkout_done_view, name='success'),
    path('checkout/', checkout_home, name='checkout'),
    path('reusecards/', payment_method_default_update_view, name='reusecard'),
    path('removecoupon/<int:id>', remove_coupon_view, name='removecoupon')
]

