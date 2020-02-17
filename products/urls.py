


from django.contrib import admin
from django.urls import path
from .views import product_list_view,ProductDetailSlugView
from .views import catogary_product_view_1,sub_catogary_product_view,sub_sub_catogary_product_view
from .views import sub_catogary_product_view_by_color,sub_sub_catogary_product_view_by_color



urlpatterns = [
   
    path('',product_list_view, name='list'),
    path('<slug:slug>/',ProductDetailSlugView.as_view(), name='detail'),
    #path('other/<slug:slug>/',OtherDetailFormView.as_view(),name='other'), 
    path('category/<slug:slug>/',catogary_product_view_1 , name='query'),
    path('sub_category/<slug:slug>/',sub_catogary_product_view , name='query1'),
    path('sub_sub_category/<slug:slug>/',sub_sub_catogary_product_view , name='query2'),
    # path('Novels',catogary_product_view_2 , name='query_1'),
    # path('instruments',catogary_product_view_3 , name='query_3'),
    # path('Accessories',catogary_product_view_4 , name='query_4'),
    path('sub_category/<slug:slug>/<color>',sub_catogary_product_view_by_color , name='query_5'),
    path('sub_sub_category/<slug:slug>/<color>',sub_sub_catogary_product_view_by_color,name='query_6'),
    
   

]

