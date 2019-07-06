from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView,FormView,DetailView,View,UpdateView
from django.utils.http import is_safe_url
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import LoginForm,RegisterForm,GuestForm,UserDetailChangeForm,SupplierRegisterForm
from .models import GuestEmail,Supplier
from .signals import user_logged_in


# Create your views here.
# @login_required  #/accounts/login/?next=/some/path/
# def account_home_view(request):
#     return render(request,"accounts/home.html",{})


 
class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/home.html'
    def get_object(self):
        return self.request.user
    
    
    


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
        context['title']='Change your details'
        return context
    def get_success_url(self):
        return reverse("account:home")



class LoginView(FormView):
    form_class=LoginForm
    success_url='/'
    template_name='accounts/login.html' 
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
                return redirect("/")
        return super(LoginView,self).form_invalid(form)



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
    success_url = '/'
    


class SupplierRegisterView(CreateView):
    model = Supplier
    form_class = SupplierRegisterForm
    template_name = 'accounts/register.html'
    success_url = '/register/'

    







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

