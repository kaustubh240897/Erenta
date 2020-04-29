from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import GuestEmail,Supplier,EmailActivation, Bank_Account_Detail

User = get_user_model()
class UserAdmin(BaseUserAdmin):
    
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin')
    list_filter = ('admin','staff','is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Full_name', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('admin','staff','is_superuser','is_active','groups','user_permissions')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email','full_name')
    ordering = ('email',)
    filter_horizontal = ('groups','user_permissions')


admin.site.register(User, UserAdmin)

   
# Remove Group Model from admin. We're not using it.
#admin.site.unregister(Group)
   
    # class Meta:
    #     model = User

class EmailActivationAdmin(admin.ModelAdmin):
    search_fields=['email']
    class Meta:
        model = EmailActivation
admin.site.register(EmailActivation, EmailActivationAdmin)

class GuestEmailAdmin(admin.ModelAdmin):
    search_fields=['email']
    class Meta:
        model = GuestEmail


admin.site.register(GuestEmail, GuestEmailAdmin)

# Register your models here.
class SupplierRegisterAdmin(admin.ModelAdmin):
    
    search_fields=['Shop_name']
    class Meta:
        model = Supplier


admin.site.register(Supplier, SupplierRegisterAdmin)
class BankRegisterAdmin(admin.ModelAdmin):
    
    search_fields=['Account_number']
    class Meta:
        model = Bank_Account_Detail
admin.site.register(Bank_Account_Detail, BankRegisterAdmin)
