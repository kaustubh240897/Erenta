from django.views.generic import ListView, DetailView,View
from django.views.generic.edit import UpdateView
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from billing.models import BillingProfile
#from django.shortcuts import render
from .models import Order,Cancel_Item
from .forms import RefundForm
from carts.forms import CouponForm,TransactionForm
from django.contrib import messages
from products.models import Product_description,Category,Sub_Category,Sub_Sub_Category
from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist
import datetime
from datetime import date
from django.utils import timezone
from django.conf import settings
from django.views.generic import CreateView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from carts.models import Cart,CartItem,Coupon,TransactionMessage
from addresses.forms import AddressForm
from addresses.models import Address
from products.models import  Variation
from accounts.models import GuestEmail
from accounts.forms import LoginForm, GuestForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
# Create your views here.

import stripe
STRIPE_SECRET_KEY = getattr( settings, "STRIPE_SECRET_KEY" , "sk_test_HOMstuXI7oONEi2EkZO0diAb0044RmXYPQ")
STRIPE_PUB_KEY = getattr( settings, "STRIPE_PUB_KEY" , 'pk_test_01sCwPKCtrJau8EiJu30FEXE00xcNv24Mm')
stripe.api_key =  STRIPE_SECRET_KEY



class OrderListView(LoginRequiredMixin,ListView):
    model = Order
    template_name = 'orders/order_list.html'
    
    
    def get_context_data(self, *args, **kwargs):
        context = super(OrderListView, self).get_context_data(*args, **kwargs)
        queryset = Order.objects.filter(billing_profile__email=self.request.user).not_created().distinct()
        queryset1 = Order.objects.filter(billing_profile__email=self.request.user, cart__cartitem__status = 'paid').not_created().distinct()
        queryset2 = Order.objects.filter(billing_profile__email=self.request.user, cart__cartitem__status = 'shipped').not_created().distinct()
        queryset3 = Order.objects.filter(billing_profile__email=self.request.user, cart__cartitem__refund_requested = True).not_created().distinct()
        queryset4 = Order.objects.filter(billing_profile__email=self.request.user, cart__cartitem__status='returned back').not_created().distinct()
        queryset5 = Order.objects.filter(billing_profile__email=self.request.user, cart__cartitem__cancel_request = True).not_created().distinct()
        
        page = self.request.GET.get('page', 1)
        paginator = Paginator(queryset, 10)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        context['paid_orders'] = 'paid orders',
        context['products'] = products
        context['paid_count'] = queryset1.count()
        context['shipped_count'] = queryset2.count()
        context['refund_count'] = queryset3.count()
        context['complete_count'] = queryset4.count()
        context['cancel_count'] = queryset5.count()
        context["category_images"] = Category.objects.all()
        context["sub_categorys"] =  Sub_Category.objects.all()
        context["sub_sub_categorys"] =  Sub_Sub_Category.objects.all()
        return context

class ShippedOrderListView(LoginRequiredMixin,ListView):
    model = Order
    template_name = 'orders/order_list.html'
    
    # def get_queryset(self):
    #     return Order.objects.by_request(self.request).not_created()
    
    def get_context_data(self, *args, **kwargs):
        context = super(ShippedOrderListView, self).get_context_data(*args, **kwargs)
        queryset = Order.objects.filter(billing_profile__email=self.request.user, cart__cartitem__status = 'shipped').not_created().distinct()
        page = self.request.GET.get('page', 1)
        paginator = Paginator(queryset, 10)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        context['shipped_orders'] = 'shippedorders',
        context['products'] = products
        return context

class RefundedOrderListView(LoginRequiredMixin,ListView):
    model = Order
    template_name = 'orders/order_list.html'
    
    # def get_queryset(self):
    #     return Order.objects.by_request(self.request).not_created()
    
    def get_context_data(self, *args, **kwargs):
        context = super(RefundedOrderListView, self).get_context_data(*args, **kwargs)
        queryset = Order.objects.filter(billing_profile__email=self.request.user, cart__cartitem__refund_requested = True).not_created().distinct()
        page = self.request.GET.get('page', 1)
        paginator = Paginator(queryset, 10)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        context['refund_orders'] = 'refundorders',
        context['products'] = products
        return context

class ReturnedOrderListView(LoginRequiredMixin,ListView):
    model = Order
    template_name = 'orders/order_list.html'
    
    # def get_queryset(self):
    #     return Order.objects.by_request(self.request).not_created()
    
    def get_context_data(self, *args, **kwargs):
        context = super(ReturnedOrderListView, self).get_context_data(*args, **kwargs)
        queryset = Order.objects.filter(billing_profile__email=self.request.user, cart__cartitem__status='returned back').not_created().distinct()
        page = self.request.GET.get('page', 1)
        paginator = Paginator(queryset, 10)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        context['returned_orders'] = 'returnedorders',
        context['products'] = products
        return context


class CancelOrderListView(LoginRequiredMixin,ListView):
    model = Order
    template_name = 'orders/order_list.html'
    
    # def get_queryset(self):
    #     return Order.objects.by_request(self.request).not_created()
    
    def get_context_data(self, *args, **kwargs):
        context = super(CancelOrderListView, self).get_context_data(*args, **kwargs)
        queryset = Order.objects.filter(billing_profile__email=self.request.user, cart__cartitem__cancel_request = True).not_created().distinct()
        page = self.request.GET.get('page', 1)
        paginator = Paginator(queryset, 10)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        context['cancelled_orders'] = 'cancelled items in orders',
        context['products'] = products
        return context


class OrderDetailView(LoginRequiredMixin,DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    def get_context_data(self, *args, **kwargs):
        context = super(OrderDetailView, self).get_context_data(*args, **kwargs)
        order_id = self.kwargs.get('order_id')
        # context['form'] = OtherDetailForm(initial={'post': self.object })
        context['title'] = 'Order Detail'
        context['paid'] = 'Paid'
        context['messages1'] = TransactionMessage.objects.filter(order_id=self.kwargs.get('order_id'))
        context['today'] = date.today()
        context["category_images"] = Category.objects.all()
        context["sub_categorys"] =  Sub_Category.objects.all()
        context["sub_sub_categorys"] =  Sub_Sub_Category.objects.all()
        #context['order_status'] = Order.objects.filter(order_id=order_id, cart__cartitem__status='shipped')
        #context['time']=Order.objects.filter(order_id=order_id,cart__cartitem__updated__gte=timezone.now() - datetime.timedelta(hours=24))
        #context['cancel_time']=Order.objects.filter(order_id=order_id,cart__cartitem__updated__lte=timezone.now() - datetime.timedelta(hours=24))
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

    def post(self,*args, **kwargs):
        
        form = TransactionForm(self.request.POST)
        if form.is_valid():
            cart_id = form.cleaned_data.get('cart_id')
            message = form.cleaned_data.get('message')
            # edit the order
            try:
                #store the refund
                reviews = TransactionMessage()
                reviews.user = self.request.user
                reviews.cart_id = cart_id
                reviews.order_id = self.kwargs.get('order_id')
                reviews.message = message
                reviews.save()
                messages.info(self.request, "Your message is sent.")
                return redirect("orders:detail", self.kwargs.get('order_id'))
            except ObjectDoesNotExist:
                messages.warning(self.request, "Sorry! This user does not exist.")
                return redirect("orders:detail", self.kwargs.get('order_id'))

class CreatedOrderView(LoginRequiredMixin,ListView):
    model =  Order
    template_name = 'orders/created_order_list.html'
    def get_queryset(self):
        
        return Order.objects.by_request(self.request).filter(status='created')

class CreatedOrderDetailView(LoginRequiredMixin,DetailView):
    model =  Order
    template_name = 'orders/order_detail.html'
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
    
    def get_context_data(self, *args, **kwargs):
        context = super(SupplierOrdersListView, self).get_context_data(*args, **kwargs)
        queryset = CartItem.objects.filter(product__user=self.request.user).distinct()
        qs_json = serializers.serialize('json', queryset)
        queryset1 = CartItem.objects.filter(product__user=self.request.user, order_confirmed = 'none', status = 'paid').distinct()
        queryset2 = CartItem.objects.filter(product__user=self.request.user, order_confirmed = 'confirmed', status = 'paid').distinct()
        queryset3 = CartItem.objects.filter(product__user=self.request.user, order_confirmed = 'confirmed', status = 'shipped').distinct()
        queryset4 = CartItem.objects.filter(product__user=self.request.user, refund_requested=True).distinct()
        queryset5 = CartItem.objects.filter(product__user=self.request.user, status='returned back',order_confirmed='confirmed').distinct()
        queryset6 = CartItem.objects.filter(product__user=self.request.user, cancel_request=True).distinct()
        page = self.request.GET.get('page', 1)
        paginator = Paginator(queryset, 50)
        # try:
        #     products = paginator.page(page)
        # except PageNotAnInteger:
        #     products = paginator.page(1)
        # except EmptyPage:
        #     products = paginator.page(paginator.num_pages)
        context['title']  = "Orders"
        context['application_orders'] = "Your Applications",
        context['application_count'] = queryset1.count()
        context['paid_count'] = queryset2.count()
        context['shipped_count'] = queryset3.count()
        context['refunded_count'] = queryset4.count()
        context['complete_count'] = queryset5.count()
        context['cancelled_count'] = queryset6.count()
        context['products'] = queryset
        context['qs_json'] = qs_json
        return context

# class SupplierOrdersApplicationListView(LoginRequiredMixin,ListView):
#     model =  Order
#     template_name = 'orders/view_orders.html'
    
#     def get_context_data(self, *args, **kwargs):
#         context = super(SupplierOrdersListView, self).get_context_data(*args, **kwargs)
#         queryset = CartItem.objects.filter(product__user=self.request.user ,order_confirmed='confirmed',status='paid').distinct()
#         page = self.request.GET.get('page', 1)
#         paginator = Paginator(queryset, 10)
#         try:
#             products = paginator.page(page)
#         except PageNotAnInteger:
#             products = paginator.page(1)
#         except EmptyPage:
#             products = paginator.page(paginator.num_pages)
#         context['paid_orders'] = "paid supplier orders",
#         context['products'] = products
#         return context

# class ShippedSupplierOrdersListView(LoginRequiredMixin,ListView):
#     model =  Order
#     template_name = 'orders/view_orders.html'
    
#     def get_context_data(self, *args, **kwargs):
#         context = super(ShippedSupplierOrdersListView, self).get_context_data(*args, **kwargs)
#         queryset = CartItem.objects.filter(product__user=self.request.user, status='shipped',order_confirmed='confirmed').distinct()
#         page = self.request.GET.get('page', 1)
#         paginator = Paginator(queryset, 10)
#         try:
#             products = paginator.page(page)
#         except PageNotAnInteger:
#             products = paginator.page(1)
#         except EmptyPage:
#             products = paginator.page(paginator.num_pages)
#         context['shipped_orders'] = 'shipped suplier orders',
#         context['products'] = products
#         return context

# class RefundedSupplierOrdersListView(LoginRequiredMixin,ListView):
#     model =  Order
#     template_name = 'orders/view_orders.html'
    
#     def get_context_data(self, *args, **kwargs):
#         context = super(RefundedSupplierOrdersListView, self).get_context_data(*args, **kwargs)
#         queryset = CartItem.objects.filter(product__user=self.request.user, refund_requested=True).distinct()
#         page = self.request.GET.get('page', 1)
#         paginator = Paginator(queryset, 10)
#         try:
#             products = paginator.page(page)
#         except PageNotAnInteger:
#             products = paginator.page(1)
#         except EmptyPage:
#             products = paginator.page(paginator.num_pages)
#         context['refunded_orders'] = 'refunded supplier oders',
#         context['products'] = products
#         return context

# class ReturnedSupplierOrdersListView(LoginRequiredMixin,ListView):
#     model =  Order
#     template_name = 'orders/view_orders.html'
    
#     def get_context_data(self, *args, **kwargs):
#         context = super(ReturnedSupplierOrdersListView, self).get_context_data(*args, **kwargs)
#         queryset = CartItem.objects.filter(product__user=self.request.user, status='returned back',order_confirmed='confirmed').distinct()
#         page = self.request.GET.get('page', 1)
#         paginator = Paginator(queryset, 10)
#         try:
#             products = paginator.page(page)
#         except PageNotAnInteger:
#             products = paginator.page(1)
#         except EmptyPage:
#             products = paginator.page(paginator.num_pages)
#         context['returned_orders'] = 'returned supplier orders',
#         context['products'] = products
#         return context

# class CancelSupplierOrdersListView(LoginRequiredMixin,ListView):
#     model =  Order
#     template_name = 'orders/view_orders.html'
    
#     def get_context_data(self, *args, **kwargs):
#         context = super(CancelSupplierOrdersListView, self).get_context_data(*args, **kwargs)
#         queryset = CartItem.objects.filter(product__user=self.request.user, cancel_request=True).distinct()
#         page = self.request.GET.get('page', 1)
#         paginator = Paginator(queryset, 10)
#         try:
#             products = paginator.page(page)
#         except PageNotAnInteger:
#             products = paginator.page(1)
#         except EmptyPage:
#             products = paginator.page(paginator.num_pages)
#         context['cancelled_orders'] = 'cancelled supplier orders',
#         context['products'] = products
#         return context


class SupplierOrderDetailView(LoginRequiredMixin,DetailView):
    model =  Order
    template_name = 'orders/supplier_order_details.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SupplierOrderDetailView, self).get_context_data(*args, **kwargs)
        # context['form'] = OtherDetailForm(initial={'post': self.object })
        context['cart_id'] = self.kwargs.get('id')
        context['messages1'] = TransactionMessage.objects.filter(cart_id=self.kwargs.get('id'))
        return context

    def get_object(self):
        qs = CartItem.objects.all().filter(
            id = self.kwargs.get('id')
        )
        if qs.count()==1:
            return qs.first()
        raise Http404
    def post(self,*args, **kwargs):
        
        form = TransactionForm(self.request.POST)
        if form.is_valid():
            cart_id = form.cleaned_data.get('cart_id')
            message = form.cleaned_data.get('message')
            # edit the order
            try:
                #store the refund
                reviews = TransactionMessage()
                reviews.user = self.request.user
                reviews.cart_id = cart_id
                reviews.order_id = Order.objects.get(cart__cartitem__id = self.kwargs.get('id'))
                reviews.message = message
                reviews.save()
                messages.info(self.request, "Your message is sent.")
                return redirect("orders:supplierorderdetail", self.kwargs.get('id'))
            except ObjectDoesNotExist:
                messages.warning(self.request, "Sorry! This user does not exist.")
                return redirect("orders:supplierorderdetail", self.kwargs.get('id'))


# def view_orders(LoginRequiredMixin,request, pk):
#     products = Product_description.objects.get(pk=self.pk)
#     myorders = SupplierOrders.objects.filter(orders=products)
#     return render(request, 'classroom/teachers/view_orders.html',{'myorders': myorders})

class RequestCancelView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        id = self.kwargs.get('id')
        form = RefundForm()
        context={
            'form': form,
            'item': CartItem.objects.get(id=id),
            'count': Cancel_Item.objects.filter(cartitem_id=id).count()
            
        }
        return render(self.request, "orders/request-refund.html" ,context)
    def post(self,*args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            #order_id = form.cleaned_data.get('order_id')
            slug = self.kwargs.get('slug')
            id = self.kwargs.get('id')
            reason = form.cleaned_data.get('reason')
            
            # edit the order
            try:
                product_id=Product_description.objects.get(slug=slug)
                product_id.save()
                product_item=CartItem.objects.get(id=id)
                #order.status = refunded
                product_item.cancel_request = True
                product_item.status = 'cancellation request'
                #product_item.line_total = None
                product_item.save()
                #store the refund
                reviews = Cancel_Item()
                reviews.product_id = product_id
                reviews.cartitem_id = id
                reviews.email = self.request.user
                reviews.reason = reason
                reviews.save()
                messages.info(self.request, "Your cancel request has been received.")
                return redirect("orders:list")
            except ObjectDoesNotExist:
                messages.warning(self.request, "This product does not exist.")
                return redirect("orders:list")


@login_required
def track_item_user_view(request,cart_id,order_id):
    try:
        item = CartItem.objects.get(id=cart_id)
        return render(request,"orders/track_user_item.html", {"item" : item, "category_images": Category.objects.all(), "sub_categorys": Sub_Category.objects.all(),"sub_sub_categorys": Sub_Sub_Category.objects.all()})
    except ObjectDoesNotExist:
        messages.info(request, "You don't have an active order")
        return redirect("orders:detail" 'order_id')


def get_coupon(request, code):
    if Coupon.objects.get(code=code):
        coupon = Coupon.objects.get(code=code)
        return coupon
    else:
        messages.info(request,"Your coupon does not exist")
        return redirect("cart:checkout")

@login_required
def add_coupon(request, cart):
    if request.method == "POST":
        form = CouponForm(request.POST or None)
        if form.is_valid():
            print("ok")
            try:
                code = form.cleaned_data.get('code')
                order_ = Order.objects.filter(billing_profile__user=request.user, cart__coupon__code=code)
                if order_.count()==0:
                    cart_ = Cart.objects.get(id=cart)
                    if not cart_.coupon:
                        cart_.coupon = get_coupon(request,code)
                        cart_.save()
                        messages.success(request,"successfully added coupon")
                        return redirect("cart:checkout")
                    else:
                        messages.warning(request,"Already added coupon")
                        return redirect("cart:checkout")
                else:
                    messages.warning(request,"Sorry! You had already added this coupon code in previous orders.")
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

@login_required
def confirm_order_view(request, order_id, cartitem_id):
    try:
        item_status = CartItem.objects.get(id=cartitem_id)
        item_status.order_confirmed = 'confirmed'
        item_status.save()
        messages.success(request, "Order is confirmed now.")
        return HttpResponseRedirect(reverse("orders:supplierorderdetail", args=(cartitem_id,)))
    except ObjectDoesNotExist:
        messages.info(request, "You do not have an active order")
        return redirect("orders:orders")

@login_required
def reject_order_view(request, order_id, cartitem_id):
    try:
        item_status = CartItem.objects.get(id=cartitem_id)
        item_status.order_confirmed = 'rejected'
        item_status.supplier_cancellation = True
        item_status.cancel_request = True
        item_status.cancel_granted = True
        item_status.status = 'rejected by supplier'
        item_status.save()
        messages.success(request, "Order is rejected now.")
        return HttpResponseRedirect(reverse("orders:supplierorderdetail", args=(cartitem_id,)))
    except ObjectDoesNotExist:
        messages.info(request, "You do not have an active order")
        return redirect("orders:orders")

@login_required
def update_status_to_shipped_view(request, order_id, cartitem_id):
    try:
        item_status = CartItem.objects.get(id=cartitem_id)
        item_status.status = 'shipped'
        item_status.shipped = True
        item_status.save()
        messages.success(request, "Item's status has been updated successfully, Thank you for shipping the Item.")
        return HttpResponseRedirect(reverse("orders:supplierorderdetail", args=(cartitem_id,)))
    except ObjectDoesNotExist:
        messages.info(request, "You do not have an active order")
        return redirect("orders:orders")
@login_required
def update_status_to_returned_view(request, order_id, cartitem_id):
    try:
        item_status = CartItem.objects.get(id=cartitem_id)
        item_status.status = 'returned back'
        item_status.save()
        messages.success(request, "Item's status has been updated successfully, Thank you for receiving the Item.")
        return HttpResponseRedirect(reverse("orders:supplierorderdetail", args=(cartitem_id,)))
    except ObjectDoesNotExist:
        messages.info(request, "You do not have an active order")
        return redirect("orders:orders")

@login_required
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
@login_required
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

@login_required
def supplier_cancellation_order_view(request, order_id, cartitem_id):
    try:
        item_status = CartItem.objects.get(id=cartitem_id)
        item_status.status = 'supplier cancelled order'
        item_status.cancel_request = True
        item_status.cancel_granted = True
        item_status.supplier_cancellation = True
        item_status.save()
        messages.success(request, "Order has been cancelled successfully.")
        return HttpResponseRedirect(reverse("orders:supplierorderdetail", args=(cartitem_id,)))
    except ObjectDoesNotExist:
        messages.info(request, "You do not have an active order")
        return redirect("orders:orders")



