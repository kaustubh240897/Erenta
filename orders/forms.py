from django import forms
from .models import Order


class RefundForm(forms.Form):
    order_id = forms.CharField()
    reason  =forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    

