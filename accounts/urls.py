from django.contrib import admin
from django.urls import path
from products.views import UserProductHistoryView
from .views import AccountHomeView, UserDetailUpdateView,AccountEmailActivateView


urlpatterns = [
   
    path('', AccountHomeView.as_view(), name='home'),
    path('email/confirm/<key>/', AccountEmailActivateView.as_view(), name='email-activate'),
    path('email/resend-activation/', AccountEmailActivateView.as_view(), name='resend-activation'),
    path('details/', UserDetailUpdateView.as_view(), name='user-update'),
    path('history/products/',UserProductHistoryView.as_view(),name='user-product-history'),
   
]

