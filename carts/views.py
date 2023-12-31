from django.conf import settings
from django.views.generic import CreateView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect,HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from .forms import CouponForm,TransactionForm
from .models import Cart,CartItem,Quantity,TransactionMessage
from addresses.forms import AddressForm
from addresses.models import Address
from billing.models import BillingProfile,Card
from notification.models import Notification,Order_Notification,Supplier_Order_Notification
from products.models import Product_description, Variation, Category, Sub_Category, Sub_Sub_Category
from orders.models import Order,Low_Quantity_Notification
from accounts.models import GuestEmail
import datetime
from datetime import timedelta,datetime
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

        # for validating the city of item
        qs = CartItem.objects.filter(cart = the_id)
        for q in qs:
            if not q.product.Current_City == request.session['city_names']:
                q.cart = None
                q.save()
                messages.warning(request, 'You have chosen item from differnt city!!')
        ## for validating the city of item
        request.session['cart_items']=cart_obj.cartitem_set.count()
        cart_obj.save()
    else:
        cart_obj=None

    return render(request,"carts/view.html", {"cart" : cart_obj, "category_images": Category.objects.all(), "sub_categorys": Sub_Category.objects.all(), "sub_sub_categorys": Sub_Sub_Category.objects.all()})

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

def remove_all_items(request):
    cartitem_obj = CartItem.objects.filter(cart=request.session['cart_id'])
    for i in cartitem_obj:
        i.cart = None
        i.save()
    messages.success(request, "All items removed successfully.")
    return redirect("cart:home")

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
    #request.session['supplier_notification_count']=Supplier_Order_Notification.objects.filter(cart__cartitem__product__user=request.user,status='paid', viewed=False).count() + Low_Quantity_Notification.objects.filter(product__user=request.user,viewed=False).count()
    request.session.set_expiry(1200000)

    product_id=request.POST.get('product_id',None)
    

    try:
        product_obj = Product_description.objects.get(id=id)
        slug = product_obj.slug
            
    except Product_description.DoesNotExist:
        print("Product does not exist now!")
        return redirect("cart:home")
    
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    cart_id = request.session.get("cart_id", None)
    print(cart_id)
    
    product_variations = []
    product_variations_id = []
    if request.method == "POST":
        qty = request.POST['qty']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        start_date = datetime.strptime(start_date, '%d-%m-%Y').date()
        end_date = datetime.strptime(end_date, '%d-%m-%Y').date()
        #print(start_date)
        y = start_date.year
        m = start_date.month
        d = start_date.day
        #y, m, d = map(int, start_date.split('-'))
        date1 = datetime(y, m, d)
        y1 = end_date.year
        m1 = end_date.month
        d1 = end_date.day
        #y, m, d = map(int, end_date.split('-'))
        date2 = datetime(y1, m1, d1)
        timedelta = date2-date1
        days = timedelta.days + 1
        print(timedelta.days+1)
        if int(qty) >0 and int(timedelta.days) >= 0:
            for item in request.POST:
                key = item
                val = request.POST[key]
                try:
                    v = Variation.objects.get(product=product_obj, category__iexact=key, title__iexact=val)
                    product_variations.append(v)
                    product_variations_id.append(v.id)
                    print("id dekhne ki kosis",v.id)
                except:
                    pass
            # check wheather inventory have the item quantity
            id_list2=[]
            q= Quantity.objects.filter(product__id=id)
            

            if q.count()>0:
                for z in q:
                    x = z.variations.all()
                    break

                if x.count()==0:
                    for c in q:
                        q1 = Quantity.objects.filter(id=c.id)
                        if q1.first().quantity-int(qty) >= 0:
                            cart_item= CartItem.objects.create(cart_id=cart_id, product_id=id)
                            if len(product_variations)>0:
                                cart_item.variations.add(*product_variations)
                            cart_item.quantity=qty
                            cart_item.start_date = start_date
                            cart_item.end_date = end_date
                            cart_item.days = days
                            cart_item.save()
                            messages.success(request, 'added Successfully !!!')
                            return redirect("products:detail",slug)
                        else:
                            messages.warning(request, 'sorry quantity is too low for this item !!!')
                            return redirect("products:detail",slug)
                
                            
                else: 
                    for y in q:
                        id_list2=[]
                        j=y.variations.all()
                        j1 = y.id
                        print("quantity model ki id",j1)
                        for z in j:
                            k=z.id
                            id_list2.append(k)
                            print("quantity model ke variation ki id",id_list2)
                            print("donolist",product_variations_id)
                            product_variations_id = sorted(product_variations_id)
                            id_list2 = sorted(id_list2)
                            if(product_variations_id==id_list2):
                                j2 = j1
                                q1 = Quantity.objects.get(id=j2)
                                if q1.quantity-int(qty) >= 0:
                                    cart_item= CartItem.objects.create(cart_id=cart_id, product_id=id)
                                    if len(product_variations)>0:
                                        cart_item.variations.add(*product_variations)
                                    cart_item.quantity=qty
                                    cart_item.start_date = start_date
                                    cart_item.end_date = end_date
                                    cart_item.days = days
                                    cart_item.save()
                                    
                                    messages.success(request, 'added Successfully !!!')
                                    return redirect("products:detail",slug)
                                else:
                                    messages.warning(request, 'sorry quantity is too low for this item !!!')
                                    return redirect("products:detail",slug)
            else:
                messages.warning(request, 'sorry no items left !!!')
                return redirect("products:detail",slug)
        else:
            messages.warning(request, 'Oops!!! you added some invalid date field or quantity.Please check and fill again!')
            return redirect("products:detail",slug)                    

    messages.warning(request, 'Sorry!!! you added some invalid field Or This color or size of product not left !!!')
    return redirect("products:detail",slug)







def checkout_home(request):
    # request.session['notification_count']=Notification.objects.filter(user=request.user, viewed=False).count() + Order_Notification.objects.filter(billing_profile__user
    # = request.user, viewed=False).count()
    # request.session['supplier_notification_count']=Supplier_Order_Notification.objects.filter(cart__cartitem__product__user=request.user,status='paid', viewed=False).count() + Low_Quantity_Notification.objects.filter(product__user=request.user,viewed=False).count()
    
    
    
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    # for validating the city of item
    qs = CartItem.objects.filter(cart = request.session['cart_id'])
    for q in qs:
        if not q.product.Current_City == request.session['city_names']:
            q.cart = None
            q.save()
            messages.warning(request, 'You have chosen item from differnt city !!!')
    ## for validating the city of item
    order_obj=None
    if cart_created or cart_obj.cartitem_set.count()==0:
        return redirect("cart:home")
    
    
    login_form = LoginForm(request=request)
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
                for t in qs:
                    t.status = 'paid'
                    t.save()
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
        "cart":cart_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs" : address_qs,
        "has_card"   : has_card,
        "publish_key": STRIPE_PUB_KEY,
        "couponform" : CouponForm(),
        "category_images": Category.objects.all(),
        "sub_categorys": Sub_Category.objects.all(),
        "sub_sub_categorys": Sub_Sub_Category.objects.all()
        
    }
    return render(request,"carts/checkout.html", context)



def checkout_done_view(request):
    request.session['supplier_notification_count']=Supplier_Order_Notification.objects.filter(cart__cartitem__product__user=request.user,status='paid', viewed=False).count() + Low_Quantity_Notification.objects.filter(product__user=request.user,viewed=False).count()
    
    return render(request, "carts/checkout-done.html", {"category_images": Category.objects.all(), "sub_categorys": Sub_Category.objects.all(), "sub_sub_categorys": Sub_Sub_Category.objects.all()})


    # cart_id = request.build_absolute_uri().split('/')
    # cart_id = cart_id[len(cart_id)-2]
    

# class TransactionMessageView(LoginRequiredMixin,View):
#     def get(self, *args, **kwargs):
#         form = TransactionForm()
#         context={
#             'form': form
#         }
#         return render(self.request, "products/supplier_review.html" ,context)


def payment_method_default_update_view(request):
    if request.method == "POST":
        id = request.POST.get('optradio')
        obj = Card.objects.get(id=id)
        obj1 = Card.objects.all().first()
        obj.default = True
        obj1.default = False
        obj1.save()
        obj.save()
        return redirect("cart:checkout")

def remove_coupon_view(request, id):
    obj = Cart.objects.get(id=id)
    obj.coupon = None
    obj.save()
    return redirect("cart:checkout")
    
        
    









