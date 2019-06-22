from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from .forms import ContactForm
from products.models import Product_description,Contact
from orders.models import order_details
from django.views.generic import ListView

def home_page(request):
    #print(request.session.get("first_name","Unknown"))
    context = {
       "title":"Shop Now!",
       "content" : "Welcome to shopnow!",
       "premium_content": "Welcome"
    }
    
    return render(request,"home_page.html",context)

def about_page(request):
    context = {
       "title":"About",
       "content":"welcome to about page"
    }
    return render(request,"home_page.html",context)

def contact_page(request):
   contact_form = ContactForm(request.POST or None)
   
   context = {
       "title":"Contact",
       "content":"welcome to contact page",
        "form": contact_form 
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






            
               

    