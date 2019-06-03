from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactForm

def home_page(request):
    #print(request.session.get("first_name","Unknown"))
    context = {
       "title":"Shop Now!",
       "content" : "Welcome to shopnow!"
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

    

   #if request.method== "POST":
       #print(request.POST)
       #print(request.POST.get('name'))
       #print(request.POST.get('email'))
       #print(request.POST.get('subject'))
       #print(request.POST.get('message'))
   if contact_form.is_valid():
       print(contact_form.cleaned_data)


   return render(request,"contact/contactform.html",context)

