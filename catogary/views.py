from django.shortcuts import render
from products.models import Product_description
from django.views.generic import ListView




def catogary_product_view_3(request):
    
    query_3 = "Instruments"
    
    print(query_3)
    if query_3 is not None:
        queryset = Product_description.objects.search(query_3)
    else:
        queryset=Product_description.objects.all()
    context = {
          'qs': queryset ,
         "title":"Products",
    }
    

    return render(request,"catogary/view.html", context)




def catogary_product_view_1(request):
    
    query = "clothing"
    
    print(query)
    if query is not None:
        queryset = Product_description.objects.search(query)
    else:
        queryset=Product_description.objects.all()
    context = {
          'qs': queryset ,
         "title":"Products",
    }
    # def get_context_data(self,*args, **kwargs):
    #     context=super(catogary_product_view ,self).get_context_data(*args, **kwargs)
    #     query=self.request.GET.get("query")
    #     context['query']=query
    #     #SearchQuery.objects.create(query=query)
    #     return context

    return render(request,"catogary/view.html", context)

def catogary_product_view_2(request):
    
    query_1 = "Novels"
    
    print(query_1)
    if query_1 is not None:
        queryset = Product_description.objects.search(query_1)
    else:
        queryset=Product_description.objects.all()
    context = {
          'qs': queryset ,
         "title":"Products",
    }
    

    return render(request,"catogary/view.html", context)


