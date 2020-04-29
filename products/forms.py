from django import forms
from .models import Product_description,ProductImage,Variation,Product_Refund
from tags.models import Tag
from carts.models import Quantity
from otherdetails.models import OtherDetails
# from django.template.defaultfilters import filesizeformat
# from django.utils.translation import ugettext_lazy as _
# from django.conf import settings



class ProductForm(forms.ModelForm): 
    

    class Meta:
        model = Product_description
        fields = ['product_name','categary','sub_categary','sub_sub_categary','brand','description','cost_per_day','discount_price','image']
    
    
    # def clean_content(self):
    #     image = self.cleaned_data['image']
    #     content_type = image.content_type.split('/')[0]
    #     if content_type in settings.CONTENT_TYPES:
    #         if content._size > settings.MAX_UPLOAD_SIZE:
    #             raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(image._size)))
    #     else:
    #         raise forms.ValidationError(_('File type is not supported'))
    #     return image

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(ProductForm, self).save(commit=False)
        #supplier.set_password(self.cleaned_data["password1"])
        #user.active=False # send confirmation email
        if commit:
            user.save()
        return user


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']

    

class ProductTagForm(forms.ModelForm):
    tag_name = forms.CharField(label='Tag name', required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter tag name relevent to the product eg-: electronic item, gadget, games, men\'s watch.'})) 
    class Meta:
        model = Tag
        fields = ['tag_name']

    # def save(self, commit=True):
    #     # Save the provided password in hashed format
    #     product = super(ProductImageForm, self).save(commit=False)
    #     #supplier.set_password(self.cleaned_data["password1"])
    #     #user.active=False # send confirmation email
    #     if commit:
    #         product.save()
    #     return product
    
class ProductVariationForm(forms.ModelForm):
    title = forms.CharField(label='Title', required=True, widget=forms.TextInput(attrs={'placeholder': 'Please enter size: (eg-: Large, Medium(for clothing) or 100 cm screen (for electronics items)) or Enter color: (eg-: Black, blue)  '})) 
    

    class Meta:
        model = Variation
        fields = ['category','title']
    

class ProductQuantityForm(forms.ModelForm):
    #variations = forms.ModelMultipleChoiceField(queryset=Variation.objects.all())
    

    class Meta:
        model = Quantity
        fields = []
    
    # def __init__(self,*args, **kwargs):
    #     super(ProductQuantityForm, self).__init__(*args, **kwargs)
    #     self.fields['variations'].queryset = Variation.objects.filter(id=id)


class ProductDetailChangeForm(forms.ModelForm):
    product_name = forms.CharField(label='product name', required=False, widget=forms.TextInput(attrs={"class":'form-control'}))
    description = forms.CharField(label='description',widget=forms.Textarea(attrs={'placeholder': 'Please enter the  description'}))
    #quantity = forms.IntegerField(label='quantity', required=False, widget=forms.NumberInput(attrs={"class":'form-control'}))
    cost_per_day = forms.DecimalField(label='cost/day', required=False, widget=forms.NumberInput(attrs={"class":'form-control'}))
    # image = forms.FileField(widget=forms.ClearableFileInput(attrs={"class":'form-control'}))


    class Meta:
        model = Product_description
        fields = ['product_name','description','cost_per_day','discount_price','image']
    


class ProductImageChangeForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']     

class ProductQuantityChangeForm(forms.ModelForm):
    class Meta:
        model = Quantity
        fields = ['quantity']       

class RatingForm(forms.Form):
    # name = forms.CharField(required=True,label='product_id')
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



class ProductRefundForm(forms.Form):
    reason  =forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))