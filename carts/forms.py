from django import forms
from django.contrib import messages

    
class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code (if any?)',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))    