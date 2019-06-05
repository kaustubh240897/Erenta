from django.shortcuts import render
from .models import Cart

# Create your views here.




def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = cart_obj.products.all()
    total=0
    for x in products:
        total += x.cost_per_day
    print(total)
    cart_obj.total=total
    cart_obj.save()
    return render(request,"carts/home.html", {})

