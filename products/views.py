from django.views.generic import ListView,DetailView,View,CreateView,FormView
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect ,get_object_or_404
from .models import Product_description,User_Review,Supplier_Review,ProductImage
from accounts.models import User
from django.urls import reverse
from analytics.mixins import ObjectViewedMixin
from carts.models import Cart
from otherdetails.models import OtherDetails
from .forms import ProductForm,ProductDetailChangeForm,RatingForm,SupplierRatingForm
from django.http import Http404
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from carts.forms import OtherDetailForm
from accounts.models import User
from django.http import HttpResponseRedirect

User = settings.AUTH_USER_MODEL

# Create your views here.
def product_list_view(request):
    queryset = Product_description.objects.all()
    context = {
        'qs': queryset ,
         "title":"Products",
    }
    return render(request,"products/product_list.html", context)

# def product_detail_view(request, slug, *args, **kwargs):
    
#     instance = Product_description.objects.get_by_slug(slug=slug)
#     if instance is None:
#         raise Http404("product doesnot exist")

    


#     context = {
#         'object': instance,
#          "title":"Products_details",
#     }
#     return render(request,"products/product_detail.html", context)

class UserProductHistoryView(LoginRequiredMixin ,ListView):
    template_name = "products/user-history.html"
    

    def get_context_data(self, *args, **kwargs):
        context = super(UserProductHistoryView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        views = request.user.objectviewed_set.by_model(Product_description, model_queryset=False)[:10]
        return views


class ProductDetailSlugView(ObjectViewedMixin ,DetailView):
    queryset = Product_description.objects.all()
    
    template_name = "products/detail.html"
    
    

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        # cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        # context['cart'] = cart_obj
        slug = self.kwargs.get('slug')
        product= Product_description.objects.get(slug=slug)
        product_id = Product_description.objects.get(slug=slug)
        # context['form'] = OtherDetailForm(initial={'post': self.object })
        context['title'] = 'Details'
        context['all']=Product_description.objects.get(slug=slug)
        context['images']=ProductImage.objects.filter(product=product)
        context['reviews']=User_Review.objects.filter(product_id=product_id)
        return context
    
    # def post(self, *args, **kwargs):
    #     print(self.request.POST)
    #     form = OtherDetailForm(self.request.POST)
    #     if form.is_valid():
    #         quantity = form.cleaned_data.get('quantity')
    #         size = form.cleaned_data.get('size')
    #         days   = form.cleaned_data.get('days')
    #         other_details = form.cleaned_data.get('other_details')
    #         # edit the order
    #         try:
                
    #             details = OtherDetails()
    #             details.user = self.request.user
    #             slug_type = self.request.build_absolute_uri().split('/')
    #             slug_type = slug_type[len(slug_type)-2]
    #             details.product = Product_description.objects.get(slug=slug_type)
    #             details.quantity = quantity
    #             details.size = size
    #             details.days = days
    #             print(days)
    #             details.other_details  = other_details
    #             print(size)
    #             details.save()
    #             messages.info(self.request, "Your details has received.")
    #             return redirect("products:detail",slug=self.kwargs.get('slug'))

    #         except ObjectDoesNotExist:
    #             messages.warning(self.request, "your details has not received.")
    #             return redirect("products:detail", slug=self.kwargs.get('slug'))
    
    

    def get_success_url(self):
        messages.success(self.request, 'added Successfully !!!')
        return reverse("products:detail",slug=self.kwargs.get('slug'))
    

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')

        #instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Product_description.objects.get(slug=slug, active=True)
        except Product_description.DoesNotExist:
            raise Http404("Not found..")
        except Product_description.MultipleObjectsReturned:
            qs = Product_description.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Uhhmmm ")
        #object_viewed_signal.send(instance.__class__, instance-instance, request=request)
        return instance



# catogaries


def catogary_product_view_4(request):
    
    query_4 = "Accessories"
    
    print(query_4)
    if query_4 is not None:
        queryset = Product_description.objects.search(query_4)
    else:
        queryset=Product_description.objects.all()
    context = {
          'qs': queryset ,
         "title":"Products",
    }
    

    return render(request,"products/view.html", context)





def catogary_product_view_3(request):
    
    query_3 = "Instruments"
    
    print(query_3)
    if query_3 is not None:
        queryset = Product_description.objects.search(query_3)
    else:
        queryset=Product_description.objects.all()
    context = {
          'qs': queryset ,
         "title":"Products",
    }
    

    return render(request,"products/view.html", context)




def catogary_product_view_1(request):
    
    query = "clothing"
    
    print(query)
    if query is not None:
        queryset = Product_description.objects.search(query)
    else:
        queryset=Product_description.objects.all()
    context = {
          'qs': queryset ,
         "title":"Products",
    }
    # def get_context_data(self,*args, **kwargs):
    #     context=super(catogary_product_view ,self).get_context_data(*args, **kwargs)
    #     query=self.request.GET.get("query")
    #     context['query']=query
    #     #SearchQuery.objects.create(query=query)
    #     return context

    return render(request,"products/view.html", context)

def catogary_product_view_2(request):
    
    query_1 = "Novels"
    
    print(query_1)
    if query_1 is not None:
        queryset = Product_description.objects.search(query_1)
    else:
        queryset=Product_description.objects.all()
    context = {
          'qs': queryset ,
         "title":"Products",
    }
    

    return render(request,"products/view.html", context)


class SupplierHomeView(LoginRequiredMixin, DetailView):
    template_name = 'products/dashboard.html'
    def get_object(self):
        return self.request.user
    


class AddProductView(LoginRequiredMixin,CreateView):
    
    model = Product_description
    form_class = ProductForm
    template_name = 'products/add_products.html'
    def form_valid(self,form):
        obj = form.save(commit=False)
        obj.user = self.request.user # logged in user is available on a view func's `request` instance
        obj.save()
        return HttpResponseRedirect(self.get_success_url())
    
        
    
    def get_success_url(self):
        messages.success(self.request, 'added Successfully !!!')
        return reverse("supplier")

        
        
    
    
    
    


class my_productsView(LoginRequiredMixin,ListView):
    model = Product_description
    template_name='products/my_products.html'
    context_object_name = 'qs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['qs'] = Product_description.objects.filter(user = self.request.user)
        print(context['qs'])
        return context
    
    


   


class ProductDetailUpdateView(LoginRequiredMixin,UpdateView):
    form_class = ProductDetailChangeForm
    model = Product_description
    template_name = 'products/product-update-view.html'
    

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')

        #instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Product_description.objects.get(slug=slug, active=True)
        except Product_description.DoesNotExist:
            raise Http404("Not found..")
        except Product_description.MultipleObjectsReturned:
            qs = Product_description.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Uhhmmm ")
        #object_viewed_signal.send(instance.__class__, instance-instance, request=request)
        return instance


    
    def get_context_data(self,*args,**kwargs):
        context = super(ProductDetailUpdateView,self).get_context_data(*args,**kwargs)
        context['title']='Change your product details'
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'Updated Successfully !!!')
        return reverse("supplier")

    




class ReviewView(View):
    def get(self, *args, **kwargs):
        form = RatingForm()
        context={
            'form': form
        }
        return render(self.request, "products/review.html" ,context)
    def post(self,*args, **kwargs):
        form = RatingForm(self.request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            rating = form.cleaned_data.get('rating')
            review   = form.cleaned_data.get('review')
            # edit the order
            try:
                product_id=Product_description.objects.get(slug=name)
                product_id.save()
                #store the refund
                reviews = User_Review()
                reviews.product_id = product_id
                reviews.email = self.request.user
                reviews.rating = rating
                reviews.review  = review
                reviews.save()
                messages.info(self.request, "Your review has received.")
                return redirect("review")
            except ObjectDoesNotExist:
                messages.warning(self.request, "This product does not exist.")
                return redirect("review")


class SupplierReviewView(View):
    def get(self, *args, **kwargs):
        form = SupplierRatingForm()
        context={
            'form': form
        }
        return render(self.request, "products/supplier_review.html" ,context)
    def post(self,*args, **kwargs):
        form = SupplierRatingForm(self.request.POST)
        if form.is_valid():
            customer = form.cleaned_data.get('customer')
            rating = form.cleaned_data.get('rating')
            review   = form.cleaned_data.get('review')
            # edit the order
            try:
                #store the refund
                reviews = Supplier_Review()
                reviews.customer = customer
                reviews.email = self.request.user
                reviews.rating = rating
                reviews.review  = review
                reviews.save()
                messages.info(self.request, "Your review has received.")
                return redirect("supplierreview")
            except ObjectDoesNotExist:
                messages.warning(self.request, "Sorry! This user does not exist.")
                return redirect("supplierreview")