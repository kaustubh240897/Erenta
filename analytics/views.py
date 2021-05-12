import datetime
from django.views.generic import ListView
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count,Avg,Sum
from django.views.generic import TemplateView,View
from django.shortcuts import render
from orders.models import Order
from products.models import Product_description,Category,Sub_Category,Sub_Sub_Category
from .models import ObjectViewed,View_Count
from django.utils import timezone
from datetime import timedelta
# Create your views here.

class SalesAjaxView(View):

    def get(self,request,*args,**kwargs):
        data = {}
        if request.user.is_staff:
            qs = Order.objects.all().by_weeks_range(weeks_ago=5, number_of_weeks=5)
            if request.GET.get('type') == 'week':
                days = 7
                start_date = timezone.now().today() - datetime.timedelta(days=days-1)
                datetime_list = []
                labels = []
                salesItems = []
                for x in range(0, days):
                    new_time = start_date + datetime.timedelta(days=x)
                    datetime_list.append(new_time)
                    labels.append(new_time.strftime("%a"))
                    new_qs = qs.filter(updated__day=new_time.day,updated__month=new_time.month).not_created()
                    day_total =  new_qs.totals_data()['total__sum'] or 0
                    salesItems.append(
                       day_total
                    )

                data['labels']= labels
                data['data']= salesItems
            if request.GET.get('type') == '4weeks':
                data['labels'] = ["Four weeks ago","Three Weeks Ago", "Two Weeks Ago", "Last Week", "This Week"]
                current = 5
                data['data'] = []
                for i in range(0, 5):
                    new_qs = qs.by_weeks_range(weeks_ago=current, number_of_weeks=1).not_created()
                    sales_total = new_qs.totals_data()['total__sum'] or 0
                    data['data'].append(sales_total)
                    current -=1

        return JsonResponse(data)


class SalesView(LoginRequiredMixin,TemplateView):
    template_name = 'analytics/sales.html'

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_staff:
            return render(self.request,"400.html",{})
        return super(SalesView,self).dispatch(*args,**kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context = super(SalesView,self).get_context_data(*args,**kwargs)
        # two_weeks_ago = timezone.now() - datetime.timedelta(days=14)
        # one_week_ago = timezone.now() - datetime.timedelta(days=7)
        qs = Order.objects.all().by_weeks_range(weeks_ago=10, number_of_weeks=10)   #(start_date=two_weeks_ago, end_date=one_week_ago)
        start_date = timezone.now().date() - datetime.timedelta(hours=24)
        end_date = timezone.now().date() + datetime.timedelta(hours=24)
        today_data = qs.by_range(start_date, end_date=end_date).get_sales_breakdown()
        context['today'] = today_data
        context['this_week'] = qs.by_weeks_range(weeks_ago=1,number_of_weeks=1).get_sales_breakdown()
        context['last_four_weeks'] = qs.by_weeks_range(weeks_ago=4, number_of_weeks=4).get_sales_breakdown()
        context["category_images"] = Category.objects.all()
        context["sub_categorys"] =  Sub_Category.objects.all()
        context["sub_sub_categorys"] =  Sub_Sub_Category.objects.all()
        
        return context





class Supplier_SalesAjaxView(View):
    def get(self,request,*args,**kwargs):
        data = {}
        if request.user:
            qs = Order.objects.all().by_weeks_range(weeks_ago=5, number_of_weeks=5)
            if request.GET.get('type') == 'week':
                days = 7
                start_date = timezone.now().today() - datetime.timedelta(days=days-1)
                datetime_list = []
                labels = []
                salesItems = []
                for x in range(0, days):
                    new_time = start_date + datetime.timedelta(days=x)
                    datetime_list.append(new_time)
                    labels.append(new_time.strftime("%a"))
                    new_qs = qs.filter(updated__day=new_time.day,updated__month=new_time.month).not_created().filter(cart__cartitem__product__user=self.request.user,cart__cartitem__refund_granted='False')#.distinct()
                    day_total =  new_qs.supplier_linetotal_data()['cart__cartitem__line_total__sum'] or 0
                    salesItems.append(
                       day_total
                    )

                data['labels']= labels
                data['data']= salesItems
            if request.GET.get('type') == '4weeks':
                data['labels'] = ["Four weeks ago","Three Weeks Ago", "Two Weeks Ago", "Last Week", "This Week"]
                current = 5
                data['data'] = []
                for i in range(0, 5):
                    new_qs = qs.by_weeks_range(weeks_ago=current, number_of_weeks=1).not_created().filter(cart__cartitem__product__user=self.request.user,cart__cartitem__refund_granted='False')#.distinct()
                    sales_total = new_qs.supplier_linetotal_data()['cart__cartitem__line_total__sum'] or 0
                    data['data'].append(sales_total)
                    current -=1

        return JsonResponse(data)

    




class Supplier_SalesView(LoginRequiredMixin,TemplateView):
    template_name = 'analytics/supplier_sales.html'

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        # if not user.is_staff:
        #     return render(self.request,"400.html",{})
        return super(Supplier_SalesView,self).dispatch(*args,**kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context = super(Supplier_SalesView,self).get_context_data(*args,**kwargs)
        # two_weeks_ago = timezone.now() - datetime.timedelta(days=14)
        # one_week_ago = timezone.now() - datetime.timedelta(days=7)
        qs = Order.objects.all().by_weeks_range(weeks_ago=10, number_of_weeks=10).filter(cart__cartitem__product__user=self.request.user,cart__cartitem__refund_granted='False')   #(start_date=two_weeks_ago, end_date=one_week_ago)
        start_date = timezone.now().date() #- datetime.timedelta(hours=24)
        end_date = timezone.now().date() + datetime.timedelta(hours=24)
        today_data = qs.by_range(start_date, end_date=end_date).get_sales_breakdown_supplier()
        context['today'] = today_data
        context['this_week'] = qs.by_weeks_range(weeks_ago=1,number_of_weeks=1).get_sales_breakdown_supplier()
        context['last_four_weeks'] = qs.by_weeks_range(weeks_ago=4, number_of_weeks=4).get_sales_breakdown_supplier()
        
        return context



    
        
