from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .forms import ContactForm
from products.models import Product_description,Contact,Subscribers,Category,Sub_Category,Sub_Sub_Category
from accounts.models import Crousel
from orders.models import Order,Low_Quantity_Notification
from carts.models import CartItem
from notification.models import Notification,Order_Notification,Supplier_Order_Notification,Order_current_status
from django.views.generic import ListView
from django.views.generic import View
from django.template.loader import get_template
from analytics.models import View_Count
import datetime
from django.utils import timezone
from .utils import render_to_pdf #created in step 4
from django.utils import translation 
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home_page(request):
    if request.user.is_authenticated:
        request.session['notification_count']=Notification.objects.filter(user=request.user, viewed=False).count() + Order_Notification.objects.filter(billing_profile__user
        = request.user, viewed=False).count() + Order_current_status.objects.filter(user=request.user, viewed=False).count()
    #print(request.session.get("first_name","Unknown"))
    
    city_name = request.build_absolute_uri().split('/')
    city_name = city_name[len(city_name)-2]
    request.session['city_names'] = city_name
    c = request.session['city_names']
    print(c)

    context = {
       "title":"Erenta!",
       "content" : "Welcome to shopnow!",
       "premium_content": "Welcome",
       "trending": View_Count.objects.all().filter(product__Current_City__iexact=c)[:8],
       "crousel_images": Crousel.objects.all(),
       "category_images": Category.objects.all(),
       "sub_categorys": Sub_Category.objects.all(),
       "sub_sub_categorys": Sub_Sub_Category.objects.all()
      
    }
    
    return render(request,"home_page.html",context)

def home_redirect(request):
    if request.session.get('city_names',None) == None:
        city = 'Tokyo'
    else:
        city = request.session['city_names']
    return redirect(f'/home/{city}')


def about_page(request):
    context = {
       "title":"About",
       "content":"welcome to about page",
       "category_images": Category.objects.all(),
       "sub_categorys": Sub_Category.objects.all(),
       "sub_sub_categorys": Sub_Sub_Category.objects.all()
    }
    return render(request,"home_page.html",context)




@login_required
def notification_page(request):
    request.session['notification_count']=Notification.objects.filter(user=request.user, viewed=False).count() + Order_Notification.objects.filter(billing_profile__user
    = request.user, viewed=False).count() + Order_current_status.objects.filter(user=request.user, viewed=False).count()
    queryset= Notification.objects.filter(user=request.user, viewed=False).order_by('-timestamp')

    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    try:
        n = paginator.page(page)
    except PageNotAnInteger:
        n = paginator.page(1)
    except EmptyPage:
        n = paginator.page(paginator.num_pages)

    
    # n2 = Order_Notification.objects.filter(billing_profile__order__cart__cartitem__product__user=request.user, viewed=False)
    context = {
       "title":"Notifications",
       "notifications": n ,
       "a":"a",
       "count": Notification.objects.filter(user=request.user, viewed=False).count(),
       "count1": Order_Notification.objects.filter(billing_profile__user = request.user, viewed=False).count(),
       "count2": Order_current_status.objects.filter(user=request.user, viewed=False).count(),
       "category_images": Category.objects.all(),
       "sub_categorys": Sub_Category.objects.all(),
       "sub_sub_categorys": Sub_Sub_Category.objects.all()
    }
    return render(request,"notification_home.html",context)



@login_required
def order_notification_page(request):
    request.session['notification_count']=Notification.objects.filter(user=request.user, viewed=False).count() + Order_Notification.objects.filter(billing_profile__user
    = request.user, viewed=False).count() + Order_current_status.objects.filter(user=request.user, viewed=False).count() 
    
    queryset = Order_Notification.objects.filter(billing_profile__user=request.user,viewed=False).order_by('-timestamp')

    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    try:
        n1 = paginator.page(page)
    except PageNotAnInteger:
        n1 = paginator.page(1)
    except EmptyPage:
        n1 = paginator.page(paginator.num_pages)
    
    context = {
       "title":"Notifications",
       
       "order_notifications": n1,
       "a1":"a",
       "count": Notification.objects.filter(user=request.user, seen=False).count(),
       "count1": Order_Notification.objects.filter(billing_profile__user = request.user, seen=False).count(),
       "count2": Order_current_status.objects.filter(user=request.user, seen=False).count(),
       "category_images": Category.objects.all(),
       "sub_categorys": Sub_Category.objects.all(),
       "sub_sub_categorys": Sub_Sub_Category.objects.all()
    }
    return render(request,"notification_home.html",context)


@login_required
def order_current_status_notification_page(request):
    request.session['notification_count']=Notification.objects.filter(user=request.user, seen=False).count() + Order_Notification.objects.filter(billing_profile__user
    = request.user, viewed=False).count() + Order_current_status.objects.filter(user=request.user, seen=False).count()

    queryset = Order_current_status.objects.filter(user=request.user, viewed=False).order_by('-timestamp')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    try:
        n2 = paginator.page(page)
    except PageNotAnInteger:
        n2 = paginator.page(1)
    except EmptyPage:
        n2 = paginator.page(paginator.num_pages)
    
    context = {
       "title":"Notifications",
       
       "item_current_status": n2,
       "a2":"a",
       "count": Notification.objects.filter(user=request.user, seen=False).count(),
       "count1": Order_Notification.objects.filter(billing_profile__user = request.user, seen=False).count(),
       "count2": Order_current_status.objects.filter(user=request.user, seen=False).count(),
       "category_images": Category.objects.all(),
       "sub_categorys": Sub_Category.objects.all(),
       "sub_sub_categorys": Sub_Sub_Category.objects.all()
    }
    return render(request,"notification_home.html",context)





@login_required
def supplier_notification_page(request):
    request.session['supplier_notification_count']=Supplier_Order_Notification.objects.filter(product__user=request.user,status='paid', viewed=False).count() + Low_Quantity_Notification.objects.filter(product__user=request.user,viewed=False).count() + Order_current_status.objects.filter(product__user=request.user, supplier_viewed=False).count()
    queryset = Supplier_Order_Notification.objects.filter(product__user=request.user,status='paid',viewed=False).order_by('-timestamp')
    
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    try:
        n2 = paginator.page(page)
    except PageNotAnInteger:
        n2 = paginator.page(1)
    except EmptyPage:
        n2 = paginator.page(paginator.num_pages)
    
    context = {
       "title":"Notifications",
       "aa":"a",
       "supplier_order_notifications":n2,
       "count": Supplier_Order_Notification.objects.filter(product__user=request.user,status='paid', seen=False).count(),
       "count1": Low_Quantity_Notification.objects.filter(product__user=request.user,seen=False).count(),
       "count2": Order_current_status.objects.filter(product__user=request.user, supplier_seen=False).count(),
       
    }
    return render(request,"supplier_order_notification_home.html",context)

@login_required
def low_quantity_notification_page(request):
    request.session['supplier_notification_count']=Supplier_Order_Notification.objects.filter(product__user=request.user,status='paid', viewed=False).count() + Low_Quantity_Notification.objects.filter(product__user=request.user,viewed=False).count() + Order_current_status.objects.filter(product__user=request.user, supplier_viewed=False).count()
    
    queryset = Low_Quantity_Notification.objects.filter(product__user=request.user,viewed=False).order_by('-timestamp')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    try:
        n3 = paginator.page(page)
    except PageNotAnInteger:
        n3 = paginator.page(1)
    except EmptyPage:
        n3 = paginator.page(paginator.num_pages)
       
    context = {
       "title":"Notifications",
       "aa1":"a",
       "low_quantity_notification":n3,
       "count": Supplier_Order_Notification.objects.filter(product__user=request.user,status='paid', seen=False).count(),
       "count1": Low_Quantity_Notification.objects.filter(product__user=request.user,seen=False).count(),
       "count2": Order_current_status.objects.filter(product__user=request.user, supplier_seen=False).count(),
       
       
       
    }
    return render(request,"supplier_order_notification_home.html",context)


@login_required
def supplier_order_current_status_notification_page(request):
    request.session['supplier_notification_count']=Supplier_Order_Notification.objects.filter(product__user=request.user,status='paid', viewed=False).count() + Low_Quantity_Notification.objects.filter(product__user=request.user,viewed=False).count() + Order_current_status.objects.filter(product__user=request.user, supplier_viewed=False).count()
    
    queryset = Order_current_status.objects.filter(product__user=request.user, supplier_viewed=False).order_by('-timestamp')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    try:
        n4 = paginator.page(page)
    except PageNotAnInteger:
        n4 = paginator.page(1)
    except EmptyPage:
        n4 = paginator.page(paginator.num_pages)

    
    context = {
       "title":"Notifications",
       "aa2":"a",
       "item_current_status": n4,
       "count": Supplier_Order_Notification.objects.filter(product__user=request.user,status='paid', seen=False).count(),
       "count1": Low_Quantity_Notification.objects.filter(product__user=request.user,seen=False).count(),
       "count2": Order_current_status.objects.filter(product__user=request.user, supplier_seen=False).count(),
       
       
       
    }
    return render(request,"supplier_order_notification_home.html",context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    
    context = {
       "title":"Contact",
       "content":"welcome to contact page",
        "form": contact_form ,
        "category_images": Category.objects.all(),
       "sub_categorys": Sub_Category.objects.all(),
       "sub_sub_categorys": Sub_Sub_Category.objects.all()
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




class GeneratePdf(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('order_id')
        order= Order.objects.get(order_id=id)
        template = get_template('billing/invoice.html')
        context = {
             'today': datetime.date.today(), 
             'time': timezone.now(),
             'amount': order.total,
            'customer_name': order.billing_profile.user.full_name,
            'email': order.billing_profile.user,
            'user': self.request.user,
            'object': Order.objects.get(order_id=id),
            'title' : "Invoice",
            
            
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


class GenerateSupplierPdf(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('order_id')
        cart_id = self.kwargs.get('id')
        order= Order.objects.get(order_id=id)
        template = get_template('billing/supplier_invoice.html')
        context = {
             'today': datetime.date.today(), 
             'time': timezone.now(),
            'customer_name': order.billing_profile.user.full_name,
            'object': Order.objects.get(order_id=id),
            'supplier': CartItem.objects.get(id=cart_id),
            'user': self.request.user,
            'title': "Invoice",
            
            
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



def landing_page(request):
    # user_language = 'ja'
    # translation.activate(user_language)
    # request.session[translation.LANGUAGE_SESSION_KEY] = user_language

    if request.method=="POST":
        if request.POST.get("form_type") == '1':
            name=request.POST.get('name')
            email=request.POST.get('email')
            subject=request.POST.get('subject')
            message=request.POST.get('message')
            contact = Contact(name=name, email=email, subject=subject, message=message)
            contact.save()
            messages.success(request, 'Thank you !!!')

        elif request.POST.get("form_type")=='2':
            email = request.POST.get('email')
            subs = Subscribers(email=email)
            subs.save()
            messages.success(request, 'Thank you !!!')
    
    
    
    return render(request,"landing_page.html")



def change_language(request):
    response = HttpResponseRedirect('/')
    if request.method == 'POST':
        language = request.POST.get('language')
        if language:
            if language != settings.LANGUAGE_CODE and [lang for lang in settings.LANGUAGES if lang[0] == language]:
                redirect_path = f'/{language}/'
            elif language == settings.LANGUAGE_CODE:
                redirect_path = '/'
            else:
                return response
            from django.utils import translation
            translation.activate(language)
            response = HttpResponseRedirect(redirect_path)
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    return response

        





    