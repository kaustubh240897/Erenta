


from django.contrib import admin
from django.urls import path
from .views import product_list_view,ProductDetailSlugView
from .views import catogary_product_view_1
from .views import catogary_product_view_2
from .views import catogary_product_view_3
from .views import catogary_product_view_4


urlpatterns = [
   
    path('',product_list_view, name='list'),
    path('<slug:slug>/',ProductDetailSlugView.as_view(), name='detail'),
    path('clothing',catogary_product_view_1 , name='query'),
    path('Novels',catogary_product_view_2 , name='query_1'),
    path('instruments',catogary_product_view_3 , name='query_3'),
    path('Accessories',catogary_product_view_4 , name='query_4'),

]

