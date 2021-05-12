from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import CreateView,FormView,DetailView,View,UpdateView
from django.utils.http import is_safe_url
from django.shortcuts import render,redirect
from .forms import LoginForm,RegisterForm,GuestForm,UserDetailChangeForm,BusinessDetailUpdateForm,ReactivationEmailForm,SupplierpersonaldetailForm,SupplierbankdetailForm,BankDetailUpdateForm
from .models import GuestEmail,Supplier,EmailActivation, Bank_Account_Detail,User
from addresses.models import Address
from billing.models import Card
from products.models import Category,Sub_Sub_Category,Sub_Category
from .signals import user_logged_in
from notification.models import Supplier_Order_Notification, Order_current_status
from orders.models import Low_Quantity_Notification
from django.db import IntegrityError
from django.http import Http404,HttpResponseForbidden
from django.utils.safestring import mark_safe
from django.views.generic.edit import FormMixin
from Ecommerce_Intern.mixins import NextUrlMixin, RequestFormAttachMixin
# Create your views here.
# @login_required  #/accounts/login/?next=/some/path/
# def account_home_view(request):
#     return render(request,"accounts/home.html",{})


@login_required
def join_us_page(request):
    request.session['supplier_notification_count']=Supplier_Order_Notification.objects.filter(product__user=request.user,status='paid', viewed=False).count() + Low_Quantity_Notification.objects.filter(product__user=request.user,viewed=False).count() + Order_current_status.objects.filter(product__user=request.user, supplier_viewed=False).count()
    context = {
       "title":"E-renta: Start lending",
       'personal_details': Supplier.objects.filter(email=request.user),
       'bank_details': Bank_Account_Detail.objects.filter(email=request.user),
       "category_images": Category.objects.all(),
       "sub_categorys": Sub_Category.objects.all(),
       "sub_sub_categorys": Sub_Sub_Category.objects.all()
       
    }
    return render(request,"accounts/join_us.html",context)


 
class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/home.html'
    def get_object(self):
        return self.request.user

    def get_context_data(self,*args,**kwargs):
        context = super(AccountHomeView,self).get_context_data(*args,**kwargs)
        context["category_images"] = Category.objects.all()
        context["sub_categorys"] =  Sub_Category.objects.all()
        context["sub_sub_categorys"] =  Sub_Sub_Category.objects.all()
        return context
    
    
    
class AccountEmailActivateView(FormMixin,View):
    success_url = '/login/'
    form_class = ReactivationEmailForm
    key = None
    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(request,"Your Email has been Confirmed,Please login.")
                return redirect("login")
            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    reset_link = reverse("password_reset")
                    msg = """ Your email has already been confirmed
                            Do you need to <a href="{link}"> reset your password</a>?""".format(link=reset_link)
                    messages.success(request, mark_safe(msg))
                    return redirect("login")
        context = {'form': self.get_form() , 'key': key, "category_images": Category.objects.all(), "sub_categorys": Sub_Category.objects.all(), "sub_sub_categorys": Sub_Sub_Category.objects.all()}
        return render(request, 'registration/activation-error.html', context)
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self,form):
        msg = """ Activation link sent, Please check your email. """
        request = self.request
        messages.success(request, msg)
        email = form.cleaned_data.get("email")
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation()
        return super(AccountEmailActivateView, self).form_valid(form)
    
    def form_invalid(self, form):
        context = {'form': form, 'key': self.key }
        return render(self.request, 'registration/activation-error.html', context)

        



def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context = {
        "form": form
    }
    #print(request.user.is_authenticated)
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    if form.is_valid():
        email = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id']= new_guest_email.id
        
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/register/")
    
    return redirect("/register/")







class UserDetailUpdateView(LoginRequiredMixin,UpdateView):
    form_class = UserDetailChangeForm
    template_name = 'accounts/detail-update-view.html'
    #succeess_url = '/account/'
    def get_object(self):
        try:
            obj= User.objects.get(email=self.request.user)
        except User.DoesNotExist:
            raise Http404("Your personal details not found..!")
        except User.MultipleObjectsReturned:
            qs = User.objects.filter(email=self.request.user, active=True)
            obj = qs.first()
        except:
            raise Http404("Uhhmmm ")
        return obj

    def get_context_data(self,*args,**kwargs):
        context = super(UserDetailUpdateView,self).get_context_data(*args,**kwargs)
        context['title']='Your profile details'
        context['addresses']=Address.objects.filter(billing_profile__user=self.request.user)
        context['cards'] = Card.objects.filter(billing_profile__user=self.request.user)
        context["category_images"] = Category.objects.all()
        context["sub_categorys"] =  Sub_Category.objects.all()
        context["sub_sub_categorys"] =  Sub_Sub_Category.objects.all()
        #context['instance'] = User.objects.filter(email=self.request.user)
        
        return context
    def get_success_url(self):
        messages.success(self.request, 'Your details updated successfully')
        return reverse("account:user-update")



class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class=LoginForm
    success_url='/'
    template_name='accounts/login.html'
    default_next = '/'

    def get_context_data(self,*args,**kwargs):
        context = super(LoginView,self).get_context_data(*args,**kwargs)
        context["category_images"] = Category.objects.all()
        context["sub_categorys"] =  Sub_Category.objects.all()
        context["sub_sub_categorys"] =  Sub_Sub_Category.objects.all()
        return context
    
    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)
        



# class SupplierLoginView(FormView):
#     form_class=LoginForm
#     success_url='/supplier/'
#     template_name='accounts/snippets/login1.html' 
#     def form_valid(self, form):
#         request = self.request
#         next_ = request.GET.get('next')
#         next_post = request.POST.get('next')
#         redirect_path = next_ or next_post or None
#         email = form.cleaned_data.get("email")
#         password = form.cleaned_data.get("password")
#         user = authenticate(request, username=email , password=password)

#         if user is not None:
#             login(request, user)
#             user_logged_in.send(user.__class__ , instance=user, request=request)
#             try: 
#                 del request.session['guest_email_id']
#             except:
#                 pass
#             if is_safe_url(redirect_path, request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect("/supplier/")
#         return super(SupplierLoginView,self).form_invalid(form)



class RegisterView(CreateView):
    form_class=RegisterForm
    template_name= 'accounts/register.html'
    success_url = '/login'

    def get_context_data(self,*args,**kwargs):
        context = super(RegisterView,self).get_context_data(*args,**kwargs)
        context["category_images"] = Category.objects.all()
        context["sub_categorys"] =  Sub_Category.objects.all()
        context["sub_sub_categorys"] =  Sub_Sub_Category.objects.all()
        
        return context

    def get_success_url(self):
        messages.warning(self.request, 'Activation link has been sent to your email address, Please confirm your email then login.')
        return reverse("login")
    

# supplier business details register form
# @login_required
# def supplier_register(request):
#     try:
#         if request.method == 'POST':
#             form = SupplierRegisterForm(request.user, request.POST)
#             if form.is_valid():
#                 product = form.save(commit=False)
#                 product.email = request.user
#                 product.save()
#                 messages.success(request, 'Your details added successfully!') 
#                 return redirect('supplier')
#             else:
#                 messages.warning(request, 'Please correct the error below.') 
#         else:
#             form = SupplierRegisterForm(request.user)
#         return render(request, 'accounts/supplier_register.html', {'form': form})
    
#     except IntegrityError:
#         return HttpResponse("Sorry!! You had already filled details with this email.Please go to update details for updating your details.")  

    

class BusinessDetailUpdateView(LoginRequiredMixin,UpdateView):
    form_class = BusinessDetailUpdateForm
    template_name = 'accounts/business-detail-update-view.html'
    
    
    def get_object(self):
        try:
            obj= Supplier.objects.get(email=self.request.user)
        except Supplier.DoesNotExist:
            raise Http404("Your personal details not found..!")
        except Supplier.MultipleObjectsReturned:
            qs = Supplier.objects.filter(email=self.request.user, active=True)
            obj = qs.first()
        except:
            raise Http404("Uhhmmm ")
        return obj

    def get_context_data(self,*args,**kwargs):
        context = super(BusinessDetailUpdateView,self).get_context_data(*args,**kwargs)
        context['title']='Update your personal details'
        context["category_images"] = Category.objects.all()
        context["sub_categorys"] =  Sub_Category.objects.all()
        context["sub_sub_categorys"] =  Sub_Sub_Category.objects.all()
        return context
    def get_success_url(self):
        messages.success(self.request, 'Your details updated successfully!') 
        return reverse("supplier")




class BankDetailUpdateView(LoginRequiredMixin,UpdateView):
    form_class = BankDetailUpdateForm
    template_name = 'accounts/business-detail-update-view.html'
    
    
    def get_object(self):
        try:
            obj= Bank_Account_Detail.objects.get(email=self.request.user)
        except Bank_Account_Detail.DoesNotExist:
            raise Http404("Your bank details not found..!")
        except Supplier.MultipleObjectsReturned:
            qs = Bank_Account_Detail.objects.filter(email=self.request.user, active=True)
            obj = qs.first()
        except:
            raise Http404("Uhhmmm ")
        return obj

    def get_context_data(self,*args,**kwargs):
        context = super(BankDetailUpdateView,self).get_context_data(*args,**kwargs)
        context['title']='Update your bank details'
        context["category_images"] = Category.objects.all()
        context["sub_categorys"] =  Sub_Category.objects.all()
        context["sub_sub_categorys"] =  Sub_Sub_Category.objects.all()
        return context
    def get_success_url(self):
        messages.success(self.request, 'Your details updated successfully!') 
        return reverse("supplier")




class AddSupplierpersonaldetailView(LoginRequiredMixin,CreateView):
    
    model = Supplier
    form_class = SupplierpersonaldetailForm
    template_name = 'accounts/supplier_personal_details.html'
    def form_valid(self,form):
        obj = form.save(commit=False)
        if Supplier.objects.filter(email=self.request.user).count()>0:
            return HttpResponseRedirect(self.get_success_url1())
        
        else:
            obj.email = self.request.user # logged in user is available on a view func's `request` instance
            obj.save()
            if Bank_Account_Detail.objects.filter(email=self.request.user).count()>0:
                return HttpResponseRedirect(self.get_success_url2())
            else:
                return HttpResponseRedirect(self.get_success_url())
    
        
    
    def get_success_url(self):
        messages.success(self.request, 'Your personal details added successfully !!!')
        return reverse("addsupplierbankdetail")
    
    def get_success_url1(self):
        messages.warning(self.request, "Your personal details are already exist")
        return reverse("addsupplierbankdetail")
    
    def get_success_url2(self):
        messages.success(self.request, "Your personal details added successfully and Your Bank details already exists.")
        return reverse("supplier")



class AddSupplierbankdetailView(LoginRequiredMixin,CreateView):
    
    model = Bank_Account_Detail
    form_class = SupplierbankdetailForm
    template_name = 'accounts/supplier_bank_details.html'
    def form_valid(self,form):
        obj = form.save(commit=False)
        if Bank_Account_Detail.objects.filter(email=self.request.user):
            return HttpResponseRedirect(self.get_success_url1())
        else:
            obj.email = self.request.user # logged in user is available on a view func's `request` instance
            #obj.supplier = self.request.user
            obj.save()
            return HttpResponseRedirect(self.get_success_url())
    
        
    
    def get_success_url(self):
        messages.success(self.request, 'Your bank details have added successfully !!!')
        return reverse("supplier")
    
    def get_success_url1(self):
        messages.warning(self.request, "Your bank details are already exists")
        return reverse("supplier")








# def login_page(request):
#     form = LoginForm(request.POST or None)
#     context = {
#         "form": form
#     }
#     #print(request.user.is_authenticated)
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None

#     if form.is_valid():
#         print(form.cleaned_data)
#         email = form.cleaned_data.get("email")
#         password = form.cleaned_data.get("password")
#         supplier = authenticate(request, email=email , password=password)

#         if supplier is not None:
#             login(request, supplier)
#             try:
#                 del request.session['guest_email_id']
#             except:
#                 pass
#             if is_safe_url(redirect_path, request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect("/")
#         else:
#             print("Error")
#     return render(request,"accounts/login.html",context)






# User = get_user_model()
# def register_page(request):
#     form = RegisterForm(request.POST or None)
#     context = {
#         "form" : form
#     }
#     if form.is_valid():
#         form.save()
    
#     return render(request,"accounts/register.html",context)

