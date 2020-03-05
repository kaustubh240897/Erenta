import datetime
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count,Avg,Sum
from django.views.generic import TemplateView,View
from django.shortcuts import render
from orders.models import Order
from django.utils import timezone
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
                    salesItems.append(0)

                data['labels']= labels
                data['data']= salesItems
            if request.GET.get('type') == '4weeks':
                data['labels'] = ["Four Weeks Ago", "Three Weeks Ago", "Two Week Ago", "This Week"]
                current = 4
                data['data'] = []
                for i in range(0, 4):
                    new_qs = qs.by_weeks_range(weeks_ago=current, number_of_weeks=1).not_created()
                    sales_total = new_qs.totals_data()['total__sum']
                    if sales_total is None:
                        sales_total = 0
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
        context['today'] = qs.by_range(start_date=timezone.now().date()).get_sales_breakdown()
        context['this_week'] = qs.by_weeks_range(weeks_ago=1,number_of_weeks=1).get_sales_breakdown()
        context['last_four_weeks'] = qs.by_weeks_range(weeks_ago=5, number_of_weeks=4).get_sales_breakdown()
        
        return context 