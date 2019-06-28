from django import forms
from .models import Product_description





class ProductForm(forms.ModelForm): 
    

    class Meta:
        model = Product_description
        fields = ['product_name','categary','sub_categary','description','quantity','cost_per_day','size','image','slug']
    
    


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(ProductForm, self).save(commit=False)
        #supplier.set_password(self.cleaned_data["password1"])
        #user.active=False # send confirmation email
        if commit:
            user.save()
        return user
    