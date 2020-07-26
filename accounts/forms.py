from django.contrib.auth import authenticate, login, get_user_model
from django import forms
from .models import Supplier,EmailActivation,Bank_Account_Detail
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()
from .signals import user_logged_in


class ReactivationEmailForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = EmailActivation.objects.email_exists(email)
        if not qs.exists():
            register_link = reverse("register")
            msg = """ This email does not exists, would you like to <a href="{link}">register</a>?
             """.format(link=register_link)
            raise forms.ValidationError(mark_safe(msg))
        return email




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
        fields = ['profile_image','full_name']


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

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        email = data.get("email")
        password = data.get("password")
        qs = User.objects.filter(email=email)
        if qs.exists():
            # user email is registered check active/email activation
            not_active = qs.filter(is_active=False)
            if not_active.exists():
                link = reverse("account:resend-activation")
                reconfirm_msg = """Go to <a href='{resend_link}'>resend confirmation email </a>
                   """.format(resend_link=link)
                # not active check email activation
                confirm_email = EmailActivation.objects.filter(email=email)
                is_confirmable = confirm_email.confirmable().exists()
                if is_confirmable:
                    msg1 = "Please check your email to confirm your account or " + reconfirm_msg.lower()
                    raise forms.ValidationError(mark_safe(msg1))
                email_confirm_exist = EmailActivation.objects.email_exists(email).exists()
                if email_confirm_exist:
                    msg2 = "Email not confirmed. " + reconfirm_msg
                    raise forms.ValidationError(mark_safe(msg2))
                if not is_confirmable and not email_confirm_qs.exists():
                    raise forms.ValidationError("This user is inactive")



        user = authenticate(request, username=email , password=password)
        if user is None:
            raise forms.ValidationError("Invalid Credentials")
        login(request,user)
        self.user = user
        #user_logged_in.send(user.__class__ , instance=user, request=request)
        # try: 
        #     del request.session['guest_email_id']
        # except:
        #     pass
        
        return data


class SupplierLoginForm(forms.Form):
    
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)

    

    
    # def form_valid(self, form):
    #     request = self.request
    #     next_ = request.GET.get('next')
    #     next_post = request.POST.get('next')
    #     redirect_path = next_ or next_post or None
    #     email = form.cleaned_data.get("email")
    #     password = form.cleaned_data.get("password")
        

    #     if user is not None:
    #         if not user.is_active:
    #             messages.error(request,"This user is inactive")
    #             return super(LoginView,self).form_invalid(form)

    #         login(request, user)
    #         user_logged_in.send(user.__class__ , instance=user, request=request)
    #         try: 
    #             del request.session['guest_email_id']
    #         except:
    #             pass
    #         if is_safe_url(redirect_path, request.get_host()):
    #             return redirect(redirect_path)
    #         else:
    #             return redirect("/")
    #     return super(LoginView,self).form_invalid(form)



class RegisterForm(UserCreationForm):
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
        user.is_active=False # send confirmation email via signals
        
        if commit:
            user.save()
        return user

    
    
class BusinessDetailUpdateForm(forms.ModelForm): 
    Shop_name = forms.CharField(label='Shop name',required=True ,widget=forms.TextInput)
    Address_Line1 = forms.CharField(label='Address Line 1',required=True ,widget=forms.TextInput)
    Postal_code = forms.CharField(label='Postal code',required=True ,widget=forms.NumberInput)
    City        = forms.CharField(label='City',required=True ,widget=forms.TextInput)
    Mobile_number = forms.CharField(label='Mobile number',required=True ,widget=forms.NumberInput)
    receive_message_time = forms.CharField(label='Message Timing(timing to receive users messages)', required=False, widget=forms.TextInput(attrs={'placeholder':'ex-: anytime or 9:00 AM to 5:00 PM'})) 
    # password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Supplier
        fields = ['Shop_name','Address_Line1','Address_Line2','Postal_code','City','Mobile_number','receive_message_time']

class BankDetailUpdateForm(forms.ModelForm): 
    Account_holder_name = forms.CharField(label='Account holder name',required=True ,widget=forms.TextInput)
    Account_number = forms.CharField(label='Account number',required=True ,widget=forms.TextInput)
    IFSC_code = forms.CharField(label='IFSC Code',required=True ,widget=forms.TextInput)

    class Meta:
        model = Bank_Account_Detail
        fields = ['Account_holder_name','Account_number','IFSC_code','Account_type']


class SupplierpersonaldetailForm(forms.ModelForm):
    MY_CHOICES = (
        ('Tokyo', 'Tokyo'),
        ('Osaka', 'Osaka'),
        ('Kyoto', 'Kyoto'),
               )
    Nick_name = forms.CharField(label='Nick name',required=True ,widget=forms.TextInput)
    Shop_name = forms.CharField(label='Shop name(if any)', widget=forms.TextInput)
    Address_Line1 = forms.CharField(label='Address Line 1',required=True ,widget=forms.TextInput)
    Address_Line2 = forms.CharField(label='Address Line 2' ,widget=forms.TextInput)
    Postal_code = forms.CharField(label='Postal code',required=True ,widget=forms.NumberInput)
    City        = forms.ChoiceField(choices = MY_CHOICES)
    Country = forms.CharField(label='Country', required=True, widget=forms.TextInput)
    Mobile_number = forms.CharField(label='Mobile number',required=True ,widget=forms.NumberInput)
    receive_message_time = forms.CharField(label="Message Timing(timing to receive customer's messages)", required=False, widget=forms.TextInput(attrs={'placeholder':'ex-: anytime or 9:00 AM to 5:00 PM'})) 

    class Meta:
        model = Supplier
        fields = ['Nick_name','Shop_name','Address_Line1','Address_Line2','Postal_code','City','Country','Mobile_number','receive_message_time']



class SupplierbankdetailForm(forms.ModelForm):
    Account_holder_name = forms.CharField(label='Account holder name',required=True, widget=forms.TextInput)
    Account_number = forms.CharField(label='Account number', required=True, widget=forms.TextInput)
    IFSC_code = forms.CharField(label='IFSC Code', required=True,widget=forms.TextInput)
    
    class Meta:
        model = Bank_Account_Detail
        fields = ['Account_holder_name', 'Account_number', 'IFSC_code', 'Account_type', ]

