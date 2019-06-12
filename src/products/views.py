from django.views.generic import ListView,DetailView
from django.shortcuts import render, get_object_or_404
from .models import Product_description
from carts.models import Cart
from django.http import Http404

# Create your views here.
def product_list_view(request):
    queryset = Product_description.objects.all()
    context = {
        'qs': queryset ,
         "title":"Products",
    }
    return render(request,"products/product_list.html", context)

# def product_detail_view(request, slug, *args, **kwargs):
    
#     instance = Product_description.objects.get_by_slug(slug=slug)
#     if instance is None:
#         raise Http404("product doesnot exist")

    


#     context = {
#         'object': instance,
#          "title":"Products_details",
#     }
#     return render(request,"products/product_detail.html", context)



class ProductDetailSlugView( DetailView):
    queryset = Product_description.objects.all()
    template_name = "products/product_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')

        #instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Product_description.objects.get(slug=slug, active=True)
        except Product_description.DoesNotExist:
            raise Http404("Not found..")
        except Product_description.MultipleObjectsReturned:
            qs = Product_description.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Uhhmmm ")
        return instance

    
    

# catogaries


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
    

    return render(request,"products/view.html", context)




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

    return render(request,"products/view.html", context)

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
    

    return render(request,"products/view.html", context)

