from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.urls import reverse
from .forms import CardForm
from django.http import Http404


import stripe
STRIPE_SECRET_KEY = getattr( settings, "STRIPE_SECRET_KEY" , "sk_test_HOMstuXI7oONEi2EkZO0diAb0044RmXYPQ")
STRIPE_PUB_KEY = getattr( settings, "STRIPE_PUB_KEY" , 'pk_test_01sCwPKCtrJau8EiJu30FEXE00xcNv24Mm')
stripe.api_key =  STRIPE_SECRET_KEY

from .models import BillingProfile, Card
def payment_method_view(request):
    if request.user.is_authenticated:
        billing_profile = request.user.billingprofile
        my_customer_id = billing_profile.customer_id
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    my_cards = Card.objects.filter(billing_profile__email=request.user)
    print(request.POST.get('optradio'))
    if not billing_profile:
        return redirect("/")
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_ , request.get_host()):
        next_url = next_
    return render(request,'billing/payment-method.html', {"publish_key": STRIPE_PUB_KEY, "next_url": next_url, 'cards': my_cards})


def payment_method_createview(request):
    if request.method == "POST" and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({"message" : "cannot find this user"}, status_code=401)
        token = request.POST.get("token")
        if token is not None:
            new_card_obj = Card.objects.add_new(billing_profile, token)
            
        return JsonResponse({"message":"Success! your card was added."})
    return HttpResponse("error", status_code=401)




class CardUpdateView(LoginRequiredMixin,UpdateView):
    form_class = CardForm
    model = Card
    template_name = 'billing/card_update_view.html'
    

    def get_object(self, *args, **kwargs):
        request = self.request
        id = self.kwargs.get('id')

        #instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Card.objects.get(id=id)
        except Card.DoesNotExist:
            raise Http404("Not found..")
        except Card.MultipleObjectsReturned:
            qs = Card.objects.filter(id=id)
            instance = qs.first()
        except:
            raise Http404("Uhhmmm ")
        #object_viewed_signal.send(instance.__class__, instance-instance, request=request)
        return instance


    
    def get_context_data(self,*args,**kwargs):
        context = super(CardUpdateView,self).get_context_data(*args,**kwargs)
        id = self.kwargs.get('id')
        context['title']="Edit your Card"
        context['name'] = Card.objects.get(id=id).billing_profile
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'Updated Successfully !!!')
        return reverse("accounts:user-update")







