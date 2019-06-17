from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

import stripe
stripe.api_key = "sk_test_HOMstuXI7oONEi2EkZO0diAb0044RmXYPQ"
STRIPE_PUB_KEY = 'pk_test_01sCwPKCtrJau8EiJu30FEXE00xcNv24Mm'

def payment_method_view(request):
    return render(request,'billing/payment-method.html', {"publish_key": STRIPE_PUB_KEY})


def payment_method_createview(request):
    if request.method == "POST" and request.is_ajax():
        print(request.POST)
        return JsonResponse({"message":"Done"})
    return HttpResponse("error", status_code=401)


