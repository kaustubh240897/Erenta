from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from .forms import ContactForm
from products.models import Product_description,Contact
from orders.models import Order
from notification.models import Notification,Order_Notification,Supplier_Order_Notification,Low_Quantity_Notification
from django.views.generic import ListView
from django.views.generic import View
from django.template.loader import get_template
import datetime
from django.utils import timezone
from .utils import render_to_pdf #created in step 4
def home_page(request):
    #print(request.session.get("first_name","Unknown"))
    

    context = {
       "title":"Shop Now!",
       "content" : "Welcome to shopnow!",
       "premium_content": "Welcome",
      
    }
    
    return render(request,"home_page.html",context)

def about_page(request):
    context = {
       "title":"About",
       "content":"welcome to about page"
    }
    return render(request,"home_page.html",context)


def notification_page(request):
    request.session['notification_count']=Notification.objects.filter(user=request.user, viewed=False).count() + Order_Notification.objects.filter(billing_profile__user
    = request.user, viewed=False).count()
    n= Notification.objects.filter(user=request.user, viewed=False)

    n1 = Order_Notification.objects.filter(billing_profile__user=request.user,viewed=False)
    # n2 = Order_Notification.objects.filter(billing_profile__order__cart__cartitem__product__user=request.user, viewed=False)
    context = {
       "title":"Notifications",
       "notifications": n ,
       "order_notifications": n1,
    }
    return render(request,"notification_home.html",context)

def supplier_notification_page(request):
    request.session['supplier_notification_count']=Supplier_Order_Notification.objects.filter(cart__cartitem__product__user=request.user,status='paid', viewed=False).count() + Low_Quantity_Notification.objects.filter(product__user=request.user,viewed=False).count()
    n2 = Supplier_Order_Notification.objects.filter(cart__cartitem__product__user=request.user,status='paid',viewed=False)
    n3 = Low_Quantity_Notification.objects.filter(product__user=request.user,viewed=False)
    
    context = {
       "title":"Notifications",
       "supplier_order_notifications": n2,
       "low_quantity_notification":n3,
       
    }
    return render(request,"supplier_order_notification_home.html",context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    
    context = {
       "title":"Contact",
       "content":"welcome to contact page",
        "form": contact_form ,
    }

    

    if request.method== "POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        contact = Contact(name=name, email=email, subject=subject, message=message)
        contact.save()
       
       
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
        
        if request.is_ajax():
            return JsonResponse({"message": "Thank You "})

    if contact_form.errors:
            errors = contact_form.errors.as_json()
            if request.is_ajax():
                return HttpResponse(errors, status=400,content_type= 'application/json')
    
    return render(request,"contact/contactform.html",context)




class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('order_id')
        order= Order.objects.get(order_id=id)
        template = get_template('billing/invoice.html')
        context = {
             'today': datetime.date.today(), 
             'time': timezone.now(),
             'amount': order.total,
            'customer_name': order.billing_profile.user.full_name,
            'object': Order.objects.get(order_id=id),
            
            
        }
        html = template.render(context)
        pdf = render_to_pdf('billing/invoice.html',context)
        if pdf:
            response =  HttpResponse(pdf,content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12345")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition']= content
            return response

        return HttpResponse("Not found")



class GenerateSupplierPdf(View):
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('order_id')
        order= Order.objects.get(order_id=id)
        template = get_template('billing/supplier_invoice.html')
        context = {
             'today': datetime.date.today(), 
             'time': timezone.now(),
            'customer_name': order.billing_profile.user.full_name,
            'object': Order.objects.get(order_id=id),
            'user': self.request.user
            
            
        }
        html = template.render(context)
        pdf = render_to_pdf('billing/supplier_invoice.html',context)
        if pdf:
            response =  HttpResponse(pdf,content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12345")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition']= content
            return response

        return HttpResponse("Not found")




    