from django.views.generic import ListView,DetailView
from django.shortcuts import render, get_object_or_404
from .models import Product_description

# Create your views here.
def product_list_view(request):
    queryset = Product_description.objects.all()
    context = {
        'qs': queryset
    }
    return render(request,"products/product_list.html", context)

def product_detail_view(request, pk=None, *args, **kwargs):
    #instance = Product_description.objects.get(pk=pk)
    instance = get_object_or_404(Product_description, pk=pk)
    context = {
        'object': instance
    }
    return render(request,"products/product_detail.html", context)

