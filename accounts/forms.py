from django import forms
from .models import Supplier
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()



class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name' ,'email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserDetailChangeForm(forms.ModelForm):
    full_name = forms.CharField(label='Name', required=False, widget=forms.TextInput(attrs={"class":'form-control'}))
    class Meta:
        model = User
        fields = ['full_name']


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password', 'is_active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]





class GuestForm(forms.Form):
    email = forms.EmailField()



class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)


class SupplierLoginForm(forms.Form):
    
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name' ,'email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        #user.is_active=False # send confirmation email
        if commit:
            user.save()
        return user






class SupplierRegisterForm(forms.ModelForm): 
    Shop_name = forms.CharField(label='Shop name',required=True ,widget=forms.TextInput)
    Address_Line1 = forms.CharField(label='Address Line 1',required=True ,widget=forms.TextInput)
    Postal_code = forms.CharField(label='Postal code',required=True ,widget=forms.NumberInput)
    City        = forms.CharField(label='City',required=True ,widget=forms.TextInput)
    Mobile_number = forms.CharField(label='Mobile number',required=True ,widget=forms.NumberInput)
    # password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Supplier
        fields = ['Shop_name','Address_Line1','Address_Line2','Postal_code','City','Mobile_number','bank_account_number','Shop_registration_number']
    
    # def clean_password2(self):
    #     # Check that the two password entries match
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Passwords don't match")
    #     return password2


    # def save(self,commit=True):
    #     # Save the provided password in hashed format
    #     user = super(SupplierRegisterForm, self).save(commit=False)
    #     user.email = self.request.user
    #     #user.active=False # send confirmation email
    #     if commit:
    #         user.save()
    #     return user
    def __init__(self, email, *args, **kwargs):
        super(SupplierRegisterForm, self).__init__(*args, **kwargs)
        #self.fields['category'].queryset = Category.objects.filter(email=email)
    
    
class BusinessDetailUpdateForm(forms.ModelForm): 
    Shop_name = forms.CharField(label='Shop name',required=True ,widget=forms.TextInput)
    Address_Line1 = forms.CharField(label='Address Line 1',required=True ,widget=forms.TextInput)
    Postal_code = forms.CharField(label='Postal code',required=True ,widget=forms.NumberInput)
    City        = forms.CharField(label='City',required=True ,widget=forms.TextInput)
    Mobile_number = forms.CharField(label='Mobile number',required=True ,widget=forms.NumberInput)
    # password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Supplier
        fields = ['Shop_name','Address_Line1','Address_Line2','Postal_code','City','Mobile_number','bank_account_number','Shop_registration_number']

