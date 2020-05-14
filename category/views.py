from django.shortcuts import render,redirect
from products.models import Product_description,Category
from django.views.generic import ListView




def category_product_view(request, slug,*args, **kwargs):
    
    try:
        query = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        print("Product does not exist now!")
        return redirect("products:list")
    
    print(query)
    if query is not None:
        queryset = Product_description.objects.filter(product__Current_City__iexact= request.session['city_names'],category=query)
    else:
        queryset=Product_description.objects.filter(product__Current_City__iexact= request.session['city_names'])
    context = {
          'qs': queryset ,
          'q': query,
          #'clothing_category': query,
         "title":"Products",
    }
    # def get_context_data(self,*args, **kwargs):
    #     context=super(category_product_view ,self).get_context_data(*args, **kwargs)
    #     query=self.request.GET.get("query")
    #     context['query']=query
    #     #SearchQuery.objects.create(query=query)
    #     return context

    return render(request,"products/view.html", context)

