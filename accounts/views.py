from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import CreateView,FormView,DetailView,View,UpdateView
from django.utils.http import is_safe_url
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import LoginForm,RegisterForm,GuestForm,UserDetailChangeForm,BusinessDetailUpdateForm,ReactivationEmailForm
from .models import GuestEmail,Supplier,EmailActivation
from .signals import user_logged_in
from django.db import IntegrityError
from django.http import Http404
from django.utils.safestring import mark_safe
from django.views.generic.edit import FormMixin
from Ecommerce_Intern.mixins import NextUrlMixin, RequestFormAttachMixin
# Create your views here.
# @login_required  #/accounts/login/?next=/some/path/
# def account_home_view(request):
#     return render(request,"accounts/home.html",{})


 
class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/home.html'
    def get_object(self):
        return self.request.user
    
    
    
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
        context = {'form': self.get_form() , 'key': key}
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
        return self.request.user
    def get_context_data(self,*args,**kwargs):
        context = super(UserDetailUpdateView,self).get_context_data(*args,**kwargs)
        context['title']='your details'
        return context
    def get_success_url(self):
        return reverse("account:home")



class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class=LoginForm
    success_url='/home'
    template_name='accounts/login.html'
    default_next = '/home'
    
    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)
        



class SupplierLoginView(FormView):
    form_class=LoginForm
    success_url='/supplier/'
    template_name='accounts/snippets/login1.html' 
    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=email , password=password)

        if user is not None:
            login(request, user)
            user_logged_in.send(user.__class__ , instance=user, request=request)
            try: 
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/supplier/")
        return super(SupplierLoginView,self).form_invalid(form)



class RegisterView(CreateView):
    form_class=RegisterForm
    template_name= 'accounts/register.html'
    success_url = '/login'
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
        obj,created= Supplier.objects.get_or_create(email=self.request.user)
        return obj

    def get_context_data(self,*args,**kwargs):
        context = super(BusinessDetailUpdateView,self).get_context_data(*args,**kwargs)
        context['title']='Register/Update your details'
        return context
    def get_success_url(self):
        messages.success(self.request, 'Your details registered/updated successfully!') 
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

