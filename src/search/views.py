from django.shortcuts import render
from products.models import Product_description
from django.views.generic import ListView
# Create your views here.

def search_product_view(request):
    method_dict=request.GET
    query = method_dict.get('q', None)
    print(query)
    if query is not None:
        queryset = Product_description.objects.filter(product_name__iexact= query)
    else:
        queryset=Product_description.objects.all()
    context = {
          'qs': queryset ,
         "title":"Products",
    }
    return render(request,"products/product_list.html", context)
