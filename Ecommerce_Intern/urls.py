"""Ecommerce_Intern URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib import admin
from django.urls import path ,include
from django.contrib.auth.views import LogoutView
from addresses.views import checkout_address_create_view, checkout_address_reuse_view
#from carts.views import cart_home
#from products.views import ProductDetailSlugView
from accounts.views import LoginView,RegisterView,guest_register_view,BusinessDetailUpdateView,join_us_page,AddSupplierbankdetailView,AddSupplierpersonaldetailView,BankDetailUpdateView
from billing.views import payment_method_view,payment_method_createview
from products.views import SupplierHomeView,AddProductView,my_productsView,ProductDetailUpdateView,ReviewView,SupplierReviewView,SupplierAddProductView,SupplierProductListView,SupplierAddProductImageView,SupplierAddProductVariationsView,SupplierAddProductQuantityView,SupplierTagView,ProductRefundView
#from carts.views import cart_detail_api_view
#from products.views import OtherDetailFormView
from analytics.views import SalesView,SalesAjaxView,Supplier_SalesView,Supplier_SalesAjaxView
from .views import home_page, about_page, contact_page,notification_page,supplier_notification_page,GeneratePdf,GenerateSupplierPdf,landing_page,home_redirect
from orders.views import RequestCancelView
from django.conf.urls.i18n import i18n_patterns
from .views import change_language
admin.site.site_header = 'ShopNow Administration'
admin.site.site_title = 'ShopNow Administration'
admin.site.index_title = 'ShopNow Administration'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('billing/payment-method/create/', payment_method_createview, name='billing-payment-method-endpoint'),
    path('change_language/', 
         change_language, 
         name='change_language'),
]


urlpatterns += i18n_patterns(
    
    
    path('', landing_page, name='landing-page'),
    path('home/',home_redirect, name='home-redirect'),
    path('home/Tokyo/',home_page, name='home'),
    path('home/Osaka/',home_page, name='home1'),
    path('home/Kyoto/',home_page, name='home2'),
    path('notification_page/',notification_page,name='notification_page'),
    path('supplier_notification_page/',supplier_notification_page,name='supplier_notification_page'),
    path('contact/',contact_page, name='contact'),
    path('notification/', include(("notification.urls", 'notification'), namespace='notification')),
    path('cart/', include(("carts.urls", 'carts'), namespace='cart')),
    path('about/',about_page, name='about'),
    path('join-us/',join_us_page,name='join_us'),
    path('accounts/',RedirectView.as_view(url='/account')),
    path('accounts/',include(("accounts.passwords.urls"))),
    path('account/',include(("accounts.urls", 'accounts'), namespace='account')),
    path('manage/sales/',SalesView.as_view(),name='sales-analytics'),
    path('manage/sales/data/',SalesAjaxView.as_view(),name='sales-analytics-data'),
    path('supplier/sales/',Supplier_SalesView.as_view(),name='supplier-sales-analytics'),
    path('supplier/sales/data/',Supplier_SalesAjaxView.as_view(),name='supplier-analytics-data'),
    path('login/',LoginView.as_view(), name='login'),
    #path('loginsupplier/',SupplierLoginView.as_view(), name='login1'),
    #path('api/cart/',cart_detail_api_view, name='api_cart'),
    path('checkout/address/create/', checkout_address_create_view, name='checkout_address_create'),
    path('checkout/address/reuse/', checkout_address_reuse_view, name='checkout_address_reuse'),
    path('register/guest/',guest_register_view, name='guest_register'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('billing/payment-method/', payment_method_view, name='billing-payment-method'),
    # path('billing/payment-method/create/', payment_method_createview, name='billing-payment-method-endpoint'),
    path('register/',RegisterView.as_view(), name='register'),
    #path('logout_page/', logout_page, name='logout_page'),
    path('settings/',RedirectView.as_view(url='/account')),
    path('products/', include(("products.urls", 'products'), namespace='products')),
    path('orders/', include(("orders.urls", 'orders'), namespace='orders')),
    path('search/', include(("search.urls", 'search'), namespace='search')),
    path('category/', include(("category.urls", 'category'), namespace='category')),
    path('supplier/',SupplierHomeView.as_view(),name='supplier'),
    path('add/',AddProductView.as_view(),name='add'),
    path('myproduct/',my_productsView.as_view(), name='myproduct'),
    path('updateproduct/<slug:slug>/',ProductDetailUpdateView.as_view(),name='update'),
    #path('products/<slug:slug>/',ProductDetailSlugView.as_view(),name='other'),
    path('request-refund/<int:id>/<slug:slug>/',RequestCancelView.as_view(),name='refund'),
    path('reviews/<int:id>/<slug:slug>/',ReviewView.as_view(),name='review'),
    path('product-refund/<int:id>/<slug:slug>/',ProductRefundView.as_view(),name='product-refund'),
    path('supplierreviews/',SupplierReviewView.as_view(),name='supplierreview'),
    path('businessdetailupdate/',BusinessDetailUpdateView.as_view(),name='businessdetailupdate'),
    path('bankdetailupdate/',BankDetailUpdateView.as_view(),name='bankdetailupdate'),
    path('addpersonaldetails/',AddSupplierpersonaldetailView.as_view(),name='addsupplierpersonaldetail'),
    path('addbankaccountdetails/',AddSupplierbankdetailView.as_view(),name='addsupplierbankdetail'),
    path('add_product/',SupplierAddProductView.as_view(),name='addproduct'),
    path('add_product_details/',SupplierProductListView.as_view(),name='addproductdetails'),
    path('add_product_details/add_image/<int:id>/',SupplierAddProductImageView.as_view(),name='productimage'),
    path('add_product_details/add_variations/<int:id>/',SupplierAddProductVariationsView.as_view(),name='productvariations'),
    path('add_product_details/add_quantity/<int:id>/',SupplierAddProductQuantityView.as_view(),name='productquantity'),
    path('add_product_details/add_tags/<int:id>/',SupplierTagView.as_view(),name='producttags'),
    path('<order_id>/pdf/',GeneratePdf.as_view(),name='pdf'),
    path('<id>/<order_id>/supplier/pdf/',GenerateSupplierPdf.as_view(),name='supplierpdf'),
    #prefix_default_language = False,


)

urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
