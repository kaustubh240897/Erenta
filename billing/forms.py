from django import forms

from .models import Card
class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = [
            'brand',
            'country',
            'exp_month',
            'exp_year',
            'last4'
             ]