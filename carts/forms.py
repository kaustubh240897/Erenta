from django import forms
from otherdetails.models import OtherDetails
from django.contrib import messages

class OtherDetailForm(forms.ModelForm): 
    

    class Meta:
        model = OtherDetails
        fields = ['product','quantity','size','days','other_details']
    
    

    def save(self,commit=True):
        # Save the provided password in hashed format
        

        user = super(OtherDetailForm, self).save(commit=False)
        #supplier.set_password(self.cleaned_data["password1"])
        #user.active=False # send confirma
        if commit:
            user.save()
            
        return user
    