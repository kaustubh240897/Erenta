from django.shortcuts import render
from products.models import Product_description
from django.views.generic import ListView
# Create your views here.

def search_product_view(request):
    method_dict=request.GET
    query = method_dict.get('q', None)
    print(query)
    if query is not None:
        queryset = Product_description.objects.filter(Current_City__iexact=request.session['city_names']).search(query)
    else:
        queryset=Product_description.objects.filter(Current_City__iexact=request.session['city_names']).order_by('?')
    context = {
          'qs': queryset ,
         "title":"Products",
         'query': query,
    }
    def get_context_data(self,*args, **kwargs):
        context=super(search_product_view ,self).get_context_data(*args, **kwargs)
        query=self.request.GET.get('q')
        context['query']=query
        #SearchQuery.objects.create(query=query)
        return context

    return render(request,"search/view.html", context)



def search_product_view_for_supplier(request):
    method_dict=request.GET
    query = method_dict.get('q', None)
    print(query)
    if query is not None:
        queryset = Product_description.objects.search(query).filter(user=request.user)
    else:
        queryset=Product_description.objects.all().filter(user=request.user)
    context = {
          'qs': queryset ,
         "title":"Products",
         "supplier": "supplier",
         'query': query,
    }
    def get_context_data(self,*args, **kwargs):
        context=super(search_product_view ,self).get_context_data(*args, **kwargs)
        query=self.request.GET.get('q')
        context['query']=query
        #SearchQuery.objects.create(query=query)
        return context

    return render(request,"search/supplier_view.html", context)
