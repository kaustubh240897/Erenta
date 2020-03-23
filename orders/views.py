from django.views.generic import ListView, DetailView,View
from django.views.generic.edit import UpdateView
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from billing.models import BillingProfile
#from django.shortcuts import render
from .models import Order,Refund
from carts.models import Coupon
from .forms import RefundForm
from carts.forms import CouponForm
from django.contrib import messages
from products.models import Product_description
from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.conf import settings
from django.views.generic import CreateView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from carts.models import Cart,CartItem
from addresses.forms import AddressForm
from addresses.models import Address
from products.models import  Variation
from accounts.models import GuestEmail
from accounts.forms import LoginForm, GuestForm
# Create your views here.

import stripe
STRIPE_SECRET_KEY = getattr( settings, "STRIPE_SECRET_KEY" , "sk_test_HOMstuXI7oONEi2EkZO0diAb0044RmXYPQ")
STRIPE_PUB_KEY = getattr( settings, "STRIPE_PUB_KEY" , 'pk_test_01sCwPKCtrJau8EiJu30FEXE00xcNv24Mm')
stripe.api_key =  STRIPE_SECRET_KEY



class OrderListView(LoginRequiredMixin,ListView):
    def get_queryset(self):
        
        return Order.objects.by_request(self.request).not_created()

class OrderDetailView(LoginRequiredMixin,DetailView):
    def get_context_data(self, *args, **kwargs):
        context = super(OrderDetailView, self).get_context_data(*args, **kwargs)
        order_id = self.kwargs.get('order_id')
        # context['form'] = OtherDetailForm(initial={'post': self.object })
        context['title'] = 'Order Detail'
        
        context['time']=Order.objects.filter(order_id=order_id,updated__gte=datetime.datetime.now() - datetime.timedelta(hours=24))
        return context

    def get_object(self):
        qs = Order.objects.by_request(
            self.request
        ).filter(
            order_id = self.kwargs.get('order_id')
        )
        if qs.count()==1:
            return qs.first()
        raise Http404

class CreatedOrderView(LoginRequiredMixin,ListView):
    model =  Order
    template_name = 'orders/created_order_list.html'
    def get_queryset(self):
        
        return Order.objects.by_request(self.request).filter(status='created')

class CreatedOrderDetailView(LoginRequiredMixin,DetailView):
    model =  Order
    template_name = 'orders/created_order_detail.html'
    def get_object(self):
        qs = Order.objects.all().filter(
            order_id = self.kwargs.get('order_id')
        )
        if qs.count()==1:
            return qs.first()
        raise Http404

class SupplierOrdersListView(LoginRequiredMixin,ListView):
    model =  Order
    template_name = 'orders/view_orders.html'
    

    def get_queryset(self):
        print(self.request.user)
        all_orders = Order.objects.filter(cart__cartitem__product__user=self.request.user).not_created().distinct()
        # doing for only one order, do it for ever order
        # for orders in all_orders:
        #     if(orders.objects.cart.products.registered_email = self.request.user):
        #         return orders 
        # all_products_in_order = all_orders[2].cart.products.all()
        #print(all_orders)
        # print(all_products_in_order[1].registered_email)
        return (all_orders)
        # return Order.objects.all().not_created()
        #return Order.objects.all().not_created().cart.products.all.filter(registered_email=self.request.user)


class SupplierOrderDetailView(LoginRequiredMixin,DetailView):
    model =  Order
    template_name = 'orders/supplier_order_details.html'
    def get_object(self):
        qs = Order.objects.all().filter(
            order_id = self.kwargs.get('order_id')
        )
        if qs.count()==1:
            return qs.first()
        raise Http404


# def view_orders(LoginRequiredMixin,request, pk):
#     products = Product_description.objects.get(pk=self.pk)
#     myorders = SupplierOrders.objects.filter(orders=products)
#     return render(request, 'classroom/teachers/view_orders.html',{'myorders': myorders})

class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context={
            'form': form
        }
        return render(self.request, "orders/request-refund.html" ,context)
    def post(self,*args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            order_id = form.cleaned_data.get('order_id')
            reason = form.cleaned_data.get('reason')
            
            # edit the order
            try:
                order=Order.objects.get(order_id=order_id)
                #order.status = refunded
                order.refund_requested = True
                order.save()
                #store the refund
                refund = Refund()
                refund.order = order
                refund.reason = reason
                refund.email  = self.request.user
                refund.save()
                messages.info(self.request, "Your request has received.")
                return redirect("refund")
            except ObjectDoesNotExist:
                messages.warning(self.request, "This order does not exist.")
                return redirect("refund")



def get_coupon(request, code):
    if Coupon.objects.get(code=code):
        coupon = Coupon.objects.get(code=code)
        return coupon
    else:
        messages.info(request,"Your coupon does not exist")
        return redirect("cart:checkout")


def add_coupon(request, cart):
    if request.method == "POST":
        form = CouponForm(request.POST or None)
        if form.is_valid():
            print("ok")
            try:
                code = form.cleaned_data.get('code')
                cart_ = Cart.objects.get(id=cart)
                if not cart_.coupon:
                    cart_.coupon = get_coupon(request,code)
                    cart_.save()
                    messages.success(request,"successfully added coupon")
                    return redirect("cart:checkout")
                else:
                    messages.warning(request,"Already added coupon")
                    return redirect("cart:checkout")

                
            except ObjectDoesNotExist:
                messages.info(request,"you donot have an valid code")
                return redirect("cart:checkout")
        else:
            messages.info(request,"you donot have an Valid coupon")
            return redirect("cart:checkout")

    




# class AddCouponView(View):
#     def get(self, *args, **kwargs):
#         order = Order.objects.get(billing_profile__user=self.request.user)
#         form = CouponForm()
#         context={
#             'couponform': form
#         }
#         return render(self.request, "order_snippet.html" ,context)
#     def post(self, *args, **kwargs):
#         form = CouponForm(self.request.POST or None)
#         if form.is_valid():
#             try:
#                 code = form.cleaned_data.get('code')
#                 order = Order.objects.get(
#                     billing_profile=self.request.user)
#                 order.coupon = get_coupon(self.request, code)
#                 order.save()
#                 messages.success(self.request, "Successfully added coupon")
#                 return redirect("cart:checkout")
#             except ObjectDoesNotExist:
#                 messages.info(self.request, "You do not have an active order")
#                 return redirect("cart:checkout")


# def created_order_checkout_home(request,order_id):
    
#     #created_order_cart_obj = Cart.objects.get(id=id)
#     #cart_obj = Cart.objects.get(request)
#     order_obj=None
#     #print(created_order_cart_obj)
#     # if cart_created or cart_obj.cartitem_set.count()==0:
#     #     return redirect("cart:home")
    
#     login_form = LoginForm()
#     guest_form = GuestForm()
#     address_form = AddressForm()
#     billing_address_id  = request.session.get("billing_address_id",None)
#     shipping_address_id = request.session.get("shipping_address_id",None)
#     #billing_address_form = AddressForm()
#     # try:
#     #     bill_id = request.session['bill_id']
#     # except:
#     #     bill_id=None 
#     billing_profile = BillingProfile.objects.get(user=request.user)
#     address_qs = None
#     has_card = False
#     if billing_profile is not None:
#         if request.user.is_authenticated:
#             address_qs = Address.objects.filter(billing_profile=billing_profile)
#         order_obj = Order.objects.get(order_id=order_id)
#         if shipping_address_id:
#             order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
#             del request.session["shipping_address_id"]
#         if billing_address_id:
#             order_obj.billing_address = Address.objects.get(id=billing_address_id)
#             del request.session["billing_address_id"]
#         if shipping_address_id or billing_address_id:
#             order_obj.save()
#         has_card = billing_profile.has_card
#     if request.method =="POST":
#         "check that order is done"

#         is_prepared = order_obj.check_done()
#         if is_prepared:
#             did_charge,crg_msg = billing_profile.charge(order_obj)
#             if did_charge:
#                 order_obj.mark_paid()
#                 request.session['cart_items']=0
#                 del request.session['cart_id']
#                 # for guest users
#                 if not billing_profile.user:
#                     billing_profile.set_cards_inactive()
#                 return redirect("cart:success")
#             else:
#                 print(crg_msg)
#                 return redirect("cart:checkout")
#     context = {
#         "object": order_obj,
#         "billing_profile": billing_profile,
#         "login_form": login_form,
#         "guest_form": guest_form,
#         "address_form": address_form,
#         "address_qs" : address_qs,
#         "has_card"   : has_card,
#         "publish_key": STRIPE_PUB_KEY,
#         "d": "difference ke liye",
        
#     }
#     return render(request,"carts/checkout.html", context)


def shipping_address_update_view(request,order_id):
    try:
        shipping_address = Order.objects.get(order_id=order_id)
        shipping_address.shipping_address = None
        shipping_address.save()
        messages.info(request, "create your shipping address")
        return redirect("cart:checkout")
    except ObjectDoesNotExist:
        messages.info(request, "You do not have an active order")
        return redirect("cart:checkout")

def billing_address_update_view(request,order_id):
    try:
        billing_address = Order.objects.get(order_id=order_id)
        billing_address.billing_address = None
        billing_address.save()
        messages.info(request, "create your billing address")
        return redirect("cart:checkout")
    except ObjectDoesNotExist:
        messages.info(request, "You do not have an active order")
        return redirect("cart:checkout")



