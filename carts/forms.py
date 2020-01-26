from django import forms
from otherdetails.models import OtherDetails
from django.contrib import messages

class OtherDetailForm(forms.ModelForm): 
    

    class Meta:
        model = OtherDetails
        fields = ['quantity','size','days','other_details']
    
    

    def save(self,commit=True):
        # Save the provided password in hashed format
        

        user = super(OtherDetailForm, self).save(commit=False)
        #supplier.set_password(self.cleaned_data["password1"])
        #user.active=False # send confirma
        if commit:
            user.save()
            
        return user
    
class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))    