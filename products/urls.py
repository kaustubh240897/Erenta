


from django.contrib import admin
from django.urls import path
from .views import product_list_view,ProductDetailSlugView,ProductImageUpdateView,my_productsimageView,my_productsquantityView,ProductQuantityUpdateView
from .views import category_product_view_1,sub_category_product_view,sub_sub_category_product_view
from .views import sub_category_product_view_by_color,sub_sub_category_product_view_by_color,remove_rentalperiod,remove_variations,remove_quantity,remove_image,remove_tags



urlpatterns = [
   
    path('',product_list_view, name='list'),
    path('<slug:slug>/',ProductDetailSlugView.as_view(), name='detail'),
    path('image/<slug:slug>/',my_productsimageView.as_view(),name='image'),
    path('quantity/<slug:slug>/',my_productsquantityView.as_view(),name='quantity'),
    path('quantity/update/<int:id>/',ProductQuantityUpdateView.as_view(),name='quantityupdate'),
    path('image/update/<int:id>/',ProductImageUpdateView.as_view(),name='imageupdate'),
    path('remove/<int:id1>/<int:id>/',remove_rentalperiod,name='remove_rentalperiod'),
    path('removevariations/<int:id1>/<int:id>/',remove_variations,name='remove_variations'),
    path('removequantity/<int:id1>/<int:id>/',remove_quantity,name='remove_quantity'),
    path('removeimage/<int:id1>/<int:id>/',remove_image,name='remove_image'),
    path('removetags/<int:id1>/<int:id>/',remove_tags,name='remove_tags'),
    #path('other/<slug:slug>/',OtherDetailFormView.as_view(),name='other'), 
    path('category/<slug:slug>/',category_product_view_1 , name='query'),
    path('sub_category/<slug:slug>/',sub_category_product_view , name='query1'),
    path('sub_sub_category/<slug:slug>/',sub_sub_category_product_view , name='query2'),
    # path('Novels',category_product_view_2 , name='query_1'),
    # path('instruments',category_product_view_3 , name='query_3'),
    # path('Accessories',category_product_view_4 , name='query_4'),
    path('sub_category/<slug:slug>/<color>',sub_category_product_view_by_color , name='query_5'),
    path('sub_sub_category/<slug:slug>/<color>',sub_sub_category_product_view_by_color,name='query_6'),
    
   

]

