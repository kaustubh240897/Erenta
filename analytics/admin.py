from django.contrib import admin
from .models import ObjectViewed, UserSession, View_Count
# Register your models here.

admin.site.register(ObjectViewed)
admin.site.register(UserSession)
admin.site.register(View_Count)
