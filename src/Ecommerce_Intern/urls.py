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

from django.contrib import admin
from django.urls import path ,include
from carts.views import cart_home
#from products.views import product_list_view, product_detail_view

from .views import home_page, about_page, contact_page, login_page,register_page
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_page, name='home'),
    path('contact/',contact_page, name='contact'),
    path('cart/',cart_home,name='cart'),
    path('about/',about_page, name='about'),
    path('login/',login_page, name='login'),
    path('register/',register_page, name='register'),
    path('products/', include(("products.urls", 'products'), namespace='products')),
    path('search/', include(("search.urls", 'search'), namespace='search')),

   
]

urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
