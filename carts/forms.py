from django import forms
from django.contrib import messages
from .models import TransactionMessage

    
class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code (if any?)',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    })) 

class TransactionForm(forms.ModelForm):
    class Meta:
        model = TransactionMessage
        fields = [
           # 'billing_profile',
           #'address_type',
            'cart_id',
            'message',
             ]