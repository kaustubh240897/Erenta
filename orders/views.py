from django.views.generic import ListView, DetailView
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from billing.models import BillingProfile
from django.shortcuts import render
from .models import Order,SupplierOrders
from products.models import Product_description
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
        return Order.objects.all().not_created()


class SupplierOrderDetailView(LoginRequiredMixin,DetailView):
    model =  Order
    template_name = 'orders/order_detail.html'
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