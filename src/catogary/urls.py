from django.contrib import admin
from django.urls import path
from .views import catogary_product_view_1
from .views import catogary_product_view_2
from .views import catogary_product_view_3


urlpatterns = [
   
    path('',catogary_product_view_1 , name='query'),
    path('1/',catogary_product_view_2 , name='query_1'),
    path('2/',catogary_product_view_3 , name='query_3'),
    

    
]

