from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class ContactForm(forms.Form):
  name=forms.CharField(
      widget=forms.TextInput(
          attrs={
              "class": "form-control",
              "placeholder":"form_full_name"
              }
              )
        )
  email=forms.EmailField(
      widget=forms.EmailInput(
          attrs={
              "class": "form-control",
              "placeholder":"your Email id"
              }
              )
        )
  
  subject=forms.CharField(
      widget=forms.TextInput(
          attrs={
              "class": "form-control",
              "placeholder":"subject"
              }
              )
        )
  
  message=forms.CharField(
      widget=forms.Textarea(
          attrs={
              'class':'form-control',
              "placeholder":"Your message"
              }
              )
        )

    #customized validation
  def clean_email(self):
      email=self.cleaned_data.get("email")
      if not "gmail.com" or not "ac.in" in email:
         raise forms.ValidationError("Email should be gmail.com or ac.in")
         return email


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)





class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label = 'Confirm Password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username has taken.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email has taken!")
        return email


    def clean(self):
        data=self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password2 != password:
            raise forms.ValidationError("Passwords must Match!!!")
        return data




