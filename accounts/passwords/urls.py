# accounts.passwords.urls.py 

from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from products.models import Category,Sub_Category,Sub_Sub_Category

urlpatterns  = [
                path('password/change/',auth_views.PasswordChangeView.as_view(extra_context={"category_images": Category.objects.all(), "sub_categorys": Sub_Category.objects.all(), "sub_sub_categorys": Sub_Sub_Category.objects.all()}), name='password_change'),
                path('password/change/done/',auth_views.PasswordChangeDoneView.as_view(extra_context={"category_images": Category.objects.all(), "sub_categorys": Sub_Category.objects.all(), "sub_sub_categorys": Sub_Sub_Category.objects.all()}), name='password_change_done'),
                path('password/reset/',auth_views.PasswordResetView.as_view(extra_context={"category_images": Category.objects.all(), "sub_categorys": Sub_Category.objects.all(), "sub_sub_categorys": Sub_Sub_Category.objects.all()}), name='password_reset'),
                path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(extra_context={"category_images": Category.objects.all(), "sub_categorys": Sub_Category.objects.all(), "sub_sub_categorys": Sub_Sub_Category.objects.all()}),name='password_reset_done'),
                path('password/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(extra_context={"category_images": Category.objects.all(), "sub_categorys": Sub_Category.objects.all(), "sub_sub_categorys": Sub_Sub_Category.objects.all()}),name='password_reset_confirm'),
                path('password/reset/complete/',auth_views.PasswordResetCompleteView.as_view(extra_context={"category_images": Category.objects.all(), "sub_categorys": Sub_Category.objects.all(), "sub_sub_categorys": Sub_Sub_Category.objects.all()}), name='password_reset_complete')
]