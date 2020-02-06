from django.urls import path
from django.contrib import admin
from .views import show_notification,delete_notification
urlpatterns = [

   path('show/<int:notification_id>', show_notification, name='show_notification'),
   path('delete/<int:notification_id>', delete_notification, name='delete_notification'),



]
