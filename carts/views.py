from django.conf import settings
from django.views.generic import CreateView
from django.shortcuts import render, redirect,HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from .models import Cart,CartItem
from addresses.forms import AddressForm
from addresses.models import Address
from billing.models import BillingProfile
from products.models import Product_description, Variation
from otherdetails.models import OtherDetails
from orders.models import Order
from accounts.models import GuestEmail
import datetime
from datetime import timedelta
from accounts.forms import LoginForm, GuestForm
from django.contrib import messages
# Create your views here.


import stripe
STRIPE_SECRET_KEY = getattr( settings, "STRIPE_SECRET_KEY" , "sk_test_HOMstuXI7oONEi2EkZO0diAb0044RmXYPQ")
STRIPE_PUB_KEY = getattr( settings, "STRIPE_PUB_KEY" , 'pk_test_01sCwPKCtrJau8EiJu30FEXE00xcNv24Mm')
stripe.api_key =  STRIPE_SECRET_KEY




# def cart_detail_api_view(request):
#      cart_obj, new_obj = Cart.objects.new_or_get(request)
#      items = [{
#          "id"           : x.id,
#          "url"          : x.get_absolute_url(),
#          "product_name" : x.product_name , 
#          "cost_per_day" : x.cost_per_day
#          }  for x in cart_obj.items.all()]
     
         
#      cart_data = {"items" : items,"subtotal" : cart_obj.subtotal , "total" : cart_obj.total }
#      return JsonResponse(cart_data)

def cart_home(request):
    try:
        the_id = request.session['cart_id']
    except:
        the_id=None 
    if the_id:
        cart_obj = Cart.objects.get(id=the_id)
        new_total = 0.00
        for item in cart_obj.cartitem_set.all():
            if item.product.discount_price:
                line_total = float(item.product.discount_price)* (item.quantity) * (item.days)
                new_total += line_total
                cart_obj.subtotal=new_total
            else:
                line_total = float(item.product.cost_per_day)* (item.quantity) * (item.days)
                new_total += line_total
                print(new_total)
                cart_obj.subtotal=new_total
        request.session['cart_items']=cart_obj.cartitem_set.count()
        cart_obj.save()
    else:
        cart_obj=None

    return render(request,"carts/view.html", {"cart" : cart_obj})

# def update_cart(request,slug):
#     request.session.set_expiry(1200000)
#     try:
#         qty = request.GET.get('qty')
#         update_qty = True
#     except:
#         qty = None
#         update_qty = False
    
#     cart_obj, new_obj = Cart.objects.new_or_get(request)
#     cart_id = request.session.get("cart_id", None)
#     cart = Cart.objects.get(id=cart_id)
#     product=None
#     try:
#         product = Product_description.objects.get(slug=slug)
        
#     except Product_description.DoesNotExist:
#         pass
#     except:
#         pass
    
#     cart_item, created = CartItem.objects.get_or_create(cart=cart,product=product)
#     if product is None:
#         cart_item.delete()
#     if update_qty and qty:
#         if int(qty) ==0:
#             cart_item.delete()
#         else:
#             cart_item.quantity=qty
#             cart_item.save()
#     else:
#         pass
#     new_total = 0.00
#     for item in cart_obj.cartitem_set.all():
#         line_total = float(item.product.cost_per_day)*(item.quantity)
#         new_total += line_total
#     print(new_total)
#     request.session['cart_items']=cart_obj.cartitem_set.count()
#     cart_obj.subtotal=new_total
#     cart_obj.save()

#     return redirect("cart:home")

def remove_cart(request,id):
    # try:
    #     cart_id = request.session['cart_id']
    #     cart = Cart.objects.get(id=cart_id)
    # except:
    #     return redirect("cart:home")
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    cartitem = CartItem.objects.get(id=id)
    cartitem.cart=None 
    cartitem.save()
    messages.success(request, 'removed Successfully !!!')
    return redirect("cart:home")

     


def add_to_cart(request,id):
    request.session.set_expiry(1200000)

    product_id=request.POST.get('product_id',None)
    
    
    try:
        product_obj = Product_description.objects.get(id=id)
            
    except Product_description.DoesNotExist:
        print("Product does not exist now!")
        return redirect("cart:home")
    
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    cart_id = request.session.get("cart_id", None)
    print(cart_id)
    
    product_variations = []
    if request.method == "POST":
        qty = request.POST['qty']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        y, m, d = map(int, start_date.split('-'))
        date1 = datetime.date(y, m, d)
        y, m, d = map(int, end_date.split('-'))
        date2 = datetime.date(y, m, d)
        timedelta = date2-date1
        days = timedelta.days + 1
        print(timedelta.days+1)
        if int(qty) >0:
            for item in request.POST:
                key = item
                val = request.POST[key]
                try:
                    v = Variation.objects.get(product=product_obj, category__iexact=key, title__iexact=val)
                    product_variations.append(v)
                    print(v)
                except:
                    pass

            cart_item= CartItem.objects.create(cart_id=cart_id, product_id=id)
            if len(product_variations)>0:
                cart_item.variations.add(*product_variations)
            cart_item.quantity=qty
            cart_item.start_date = start_date
            cart_item.end_date = end_date
            cart_item.days = days
            cart_item.save()

                
            
                # if request.is_ajax():
                #     print("ajax request")
                #     json_data = {
                #         "added": added,
                #         "removed": not added,
                #         "cartItemCount":cart_obj.cartitem_set.count()
                #     }
                #     return JsonResponse(json_data, status=200)
            messages.success(request, 'added Successfully !!!')
            return redirect("cart:home")
    
    messages.success(request, 'error occured !!!')
    return redirect("cart:home")







def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj=None
    if cart_created or cart_obj.cartitem_set.count()==0:
        return redirect("cart:home")
    
    
    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_id  = request.session.get("billing_address_id",None)
    shipping_address_id = request.session.get("shipping_address_id",None)
    #billing_address_form = AddressForm()

    billing_profile,billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    has_card = False
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile,cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if shipping_address_id or billing_address_id:
            order_obj.save()
        has_card = billing_profile.has_card
    if request.method =="POST":
        "check that order is done"

        is_prepared = order_obj.check_done()
        if is_prepared:
            did_charge,crg_msg = billing_profile.charge(order_obj)
            if did_charge:
                order_obj.mark_paid()
                request.session['cart_items']=0
                del request.session['cart_id']
                # for guest users
                if not billing_profile.user:
                    billing_profile.set_cards_inactive()
                return redirect("cart:success")
            else:
                print(crg_msg)
                return redirect("cart:checkout")
    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs" : address_qs,
        "has_card"   : has_card,
        "publish_key": STRIPE_PUB_KEY,
        
    }
    return render(request,"carts/checkout.html", context)



def checkout_done_view(request):
    return render(request, "carts/checkout-done.html", {})




