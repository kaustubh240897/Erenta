from django.views.generic import ListView
from django.shortcuts import render
from .models import Product_description

# Create your views here.
def product_list_view(request):
    queryset = Product_description.objects.all()
    context = {
        'qs': queryset
    }
    return render(request,"products/product_list.html", context)

