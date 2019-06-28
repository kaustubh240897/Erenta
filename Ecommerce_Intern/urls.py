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
#from products.views import product_list_view, product_detail_view
from accounts.views import LoginView,RegisterView,guest_register_view,SupplierRegisterView,SupplierLoginView
from billing.views import payment_method_view,payment_method_createview
from products.views import SupplierHomeView,AddProductView
from carts.views import cart_detail_api_view
from .views import home_page, about_page, contact_page
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_page, name='home'),
    path('contact/',contact_page, name='contact'),
    path('cart/', include(("carts.urls", 'carts'), namespace='cart')),
    path('about/',about_page, name='about'),
    path('accounts/',RedirectView.as_view(url='/account')),
    path('accounts/',include(("accounts.passwords.urls"))),
    path('account/',include(("accounts.urls", 'accounts'), namespace='account')),
    path('login/',LoginView.as_view(), name='login'),
    path('loginsupplier/',SupplierLoginView.as_view(), name='login'),
    path('api/cart/',cart_detail_api_view, name='api_cart'),
    path('checkout/address/create/', checkout_address_create_view, name='checkout_address_create'),
    path('checkout/address/reuse/', checkout_address_reuse_view, name='checkout_address_reuse'),
    path('register/guest/',guest_register_view, name='guest_register'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('billing/payment-method/', payment_method_view, name='billing-payment-method'),
    path('billing/payment-method/create/', payment_method_createview, name='billing-payment-method-endpoint'),
    path('register/',RegisterView.as_view(), name='register'),
    path('registersupplier/', SupplierRegisterView.as_view(), name='supplierregister'),
    path('settings/',RedirectView.as_view(url='/account')),
    path('products/', include(("products.urls", 'products'), namespace='products')),
    path('orders/', include(("orders.urls", 'orders'), namespace='orders')),
    path('search/', include(("search.urls", 'search'), namespace='search')),
    path('catogary/', include(("catogary.urls", 'catogary'), namespace='catogary')),
    path('supplier/',SupplierHomeView.as_view(),name='supplier'),
    path('add/',AddProductView.as_view(),name='add')

   
]

urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
