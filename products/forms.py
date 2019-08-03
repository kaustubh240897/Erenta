from django import forms
from .models import Product_description





class ProductForm(forms.ModelForm): 
    

    class Meta:
        model = Product_description
        fields = ['product_name','categary','sub_categary','brand','description','quantity','cost_per_day','size','image','registered_email']
    
    
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(ProductForm, self).save(commit=False)
        #supplier.set_password(self.cleaned_data["password1"])
        #user.active=False # send confirmation email
        if commit:
            user.save()
        return user



class ProductDetailChangeForm(forms.ModelForm):
    product_name = forms.CharField(label='product_name', required=False, widget=forms.TextInput(attrs={"class":'form-control'}))
    description = forms.CharField(label='description',widget=forms.Textarea(attrs={'placeholder': 'Please enter the  description'}))
    quantity = forms.IntegerField(label='quantity', required=False, widget=forms.NumberInput(attrs={"class":'form-control'}))
    cost_per_day = forms.DecimalField(label='cost_per_day', required=False, widget=forms.NumberInput(attrs={"class":'form-control'}))
    # image = forms.FileField(widget=forms.ClearableFileInput(attrs={"class":'form-control'}))


    class Meta:
        model = Product_description
        fields = ['product_name','description','quantity','cost_per_day','image']
    
    

class RatingForm(forms.Form):
    id = forms.CharField(required=True,label='product_id')
    rating  = forms.ChoiceField(choices=[(x, x) for x in range(1, 6)])
    review  =forms.CharField(required=True,widget=forms.Textarea(attrs={
        'rows': 4
    }))
    
class SupplierRatingForm(forms.Form):
    customer = forms.EmailField(required=True,label='customer email')
    rating  = forms.ChoiceField(choices=[(x, x) for x in range(1, 6)])
    review  =forms.CharField(required=True,widget=forms.Textarea(attrs={
        'rows': 4
    }))


    
