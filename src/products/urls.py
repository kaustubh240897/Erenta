


from django.contrib import admin
from django.urls import path
from .views import product_list_view,ProductDetailSlugView


urlpatterns = [
   
    path('',product_list_view, name='list'),
    path('<slug:slug>/',ProductDetailSlugView.as_view(), name='detail')
]

