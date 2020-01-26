from django.views.generic import ListView, DetailView,View
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from billing.models import BillingProfile
from django.shortcuts import render
from .models import Order,Refund
from carts.models import Coupon
from .forms import RefundForm
from carts.forms import CouponForm
from django.contrib import messages
from products.models import Product_description
from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

class OrderListView(LoginRequiredMixin,ListView):
    def get_queryset(self):
        
        return Order.objects.by_request(self.request).not_created()

class OrderDetailView(LoginRequiredMixin,DetailView):
    def get_object(self):
        qs = Order.objects.by_request(
            self.request
        ).filter(
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
            email   = form.cleaned_data.get('email')
            # edit the order
            try:
                order=Order.objects.get(order_id=order_id)
                order.refund_requested = True
                order.save()
                #store the refund
                refund = Refund()
                refund.order = order
                refund.reason = reason
                refund.email  = email
                refund.save()
                messages.info(self.request, "Your request has received.")
                return redirect("refund")
            except ObjectDoesNotExist:
                messages.warning(self.request, "This order does not exist.")
                return redirect("refund")



def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request,"Your coupon does not exist")
        return redirect("cart:checkout")


class AddCouponView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(billing_profile__user=self.request.user)
        form = CouponForm()
        context={
            'couponform': form
        }
        return render(self.request, "order_snippet.html" ,context)
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    billing_profile=self.request.user)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("cart:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("cart:checkout")