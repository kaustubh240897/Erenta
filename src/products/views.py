from django.views.generic import ListView,DetailView
from django.shortcuts import render, get_object_or_404
from .models import Product_description
from django.http import Http404

# Create your views here.
def product_list_view(request):
    queryset = Product_description.objects.all()
    context = {
        'qs': queryset ,
         "title":"Products",
    }
    return render(request,"products/product_list.html", context)

def product_detail_view(request, slug, *args, **kwargs):
    
    instance = Product_description.objects.get_by_slug(slug=slug)
    if instance is None:
        raise Http404("product doesnot exist")

    

    context = {
        'object': instance,
         "title":"Products_details",
    }
    return render(request,"products/product_detail.html", context)

