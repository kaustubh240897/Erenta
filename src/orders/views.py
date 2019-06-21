from django.shortcuts import render
from .models import Order

# Create your views here.
def order_details(request):
    if request.method== "POST":
       
       quantity=request.POST.get('quantity')
       size=request.POST.get('size')
       days=request.POST.get('days')
       
       order = Order(quantity=quantity, size=size,days=days)
       order.save()

       return render(request,"products/product_detail.html",{})
    