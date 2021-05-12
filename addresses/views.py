from django.shortcuts import render,redirect
from django.utils.http import is_safe_url
from .forms import AddressForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.urls import reverse
from billing.models import BillingProfile
from products.models import Category,Sub_Sub_Category,Sub_Category
from .models import Address
from django.http import Http404

def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    context = {
        "form": form,
        "category_images": Category.objects.all(),
        "sub_categorys": Sub_Category.objects.all(), 
        "sub_sub_categorys": Sub_Sub_Category.objects.all()
    }
    #print(request.user.is_authenticated)
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        print(request.POST)
        instance = form.save(commit=False)
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if billing_profile is not None:
            address_type = request.POST.get('address_type','shipping')
            instance.billing_profile= billing_profile
            instance.address_type = address_type
            instance.save()
            request.session[address_type + "_address_id"]=instance.id
            print(address_type + "_address_id")
   

        else:
            print("Error here")
            return redirect("cart:checkout")

        
        if is_safe_url(redirect_path, request.get_host()):
             return redirect(redirect_path)
        
    return redirect("cart:checkout")




def checkout_address_reuse_view(request):
    if request.user.is_authenticated:
        context = {}    
        #print(request.user.is_authenticated)
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if request.method == "POST":
            print(request.POST)
            shipping_address=request.POST.get('shipping_address', None)
            address_type = request.POST.get('address_type','shipping')
            billing_profile, billing_profile_created =BillingProfile.objects.new_or_get(request)
            
            if shipping_address is not None:
                qs = Address.objects.filter(billing_profile=billing_profile, id=shipping_address)
                if qs.exists():
                    request.session[address_type + "_address_id"] = shipping_address
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
       
    return redirect("cart:checkout")


class AddressUpdateView(LoginRequiredMixin,UpdateView):
    form_class = AddressForm
    model = Address
    template_name = 'addresses/address_update_view.html'
    

    def get_object(self, *args, **kwargs):
        request = self.request
        id = self.kwargs.get('id')

        #instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Address.objects.get(id=id)
        except Address.DoesNotExist:
            raise Http404("Not found..")
        except Address.MultipleObjectsReturned:
            qs = Address.objects.filter(id=id)
            instance = qs.first()
        except:
            raise Http404("Uhhmmm ")
        #object_viewed_signal.send(instance.__class__, instance-instance, request=request)
        return instance


    
    def get_context_data(self,*args,**kwargs):
        context = super(AddressUpdateView,self).get_context_data(*args,**kwargs)
        id = self.kwargs.get('id')
        context['title']="Edit your Address"
        context['name'] = Address.objects.get(id=id).billing_profile
        context["category_images"] = Category.objects.all()
        context["sub_categorys"] =  Sub_Category.objects.all()
        context["sub_sub_categorys"] =  Sub_Sub_Category.objects.all()
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'Updated Successfully !!!')
        return reverse("accounts:user-update")




