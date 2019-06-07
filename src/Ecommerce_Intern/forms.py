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




