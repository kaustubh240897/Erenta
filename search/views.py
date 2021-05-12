from django.shortcuts import render
from products.models import Product_description,Category,Sub_Sub_Category,Sub_Category
from django.views.generic import ListView
from analytics.models import View_Count
# Create your views here.

def search_product_view(request):
    if request.session.get('city_names',None) == None:
        request.session['city_names'] = "Tokyo"
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
         'trending':View_Count.objects.filter(product__Current_City__iexact=request.session['city_names'])[:7],
         "category_images": Category.objects.all(),
        "sub_categorys": Sub_Category.objects.all(),
        "sub_sub_categorys": Sub_Sub_Category.objects.all()

    }
    def get_context_data(self,*args, **kwargs):
        context=super(search_product_view ,self).get_context_data(*args, **kwargs)
        query=self.request.GET.get('q')
        context['query']=query
        #SearchQuery.objects.create(query=query)
        return context

    return render(request,"search/view.html", context)



def search_product_view_for_supplier(request):
    if request.session.get('city_names',None) == None:
        request.session['city_names'] = "Tokyo"
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
