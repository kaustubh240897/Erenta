from django.views.generic import ListView,DetailView,View,CreateView,FormView
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect ,get_object_or_404
from .models import Product_description,User_Review,Supplier_Review,ProductImage,Category,Sub_Category,Sub_Sub_Category,ProductImage,Variation,Quantity
from accounts.models import User
from django.urls import reverse
from analytics.mixins import ObjectViewedMixin
from carts.models import Cart
from otherdetails.models import OtherDetails
from .forms import ProductForm,ProductDetailChangeForm,RatingForm,SupplierRatingForm,ProductImageForm,ProductVariationForm,ProductQuantityForm
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

# pricing sort

# def sort_product_view_increase(self,categary,request):
#     categary = self.request.get(categary)
#     categary= Product_description.objects.get(categary=categary)
#     queryset1 = Product_description.objects.filter(categary=categary).order_by('cost_per_day')
    
#     context = {
#           'qs1': queryset1 ,
#          "title":"Sorted Products",
#     }
    

#     return render(request,"products/view.html", context)


# catogaries






def sub_catogary_product_view_by_color(request,slug, color):
    slug_type = request.build_absolute_uri().split('/')
    slug_type = slug_type[len(slug_type)-2]
    print(slug_type)
    try:
        sub_cat_query = Sub_Category.objects.get(slug=slug)
    except Sub_Category.DoesNotExist:
        print("Product does not exist now!")
        return redirect("products:list")
    
    if sub_cat_query is not None:
        queryset = Product_description.objects.filter(sub_categary=sub_cat_query, variation__title=color)
    else:
        queryset=Product_description.objects.all()
    context = {
          'qs': queryset ,
          'slug': slug_type,
         "title":"Products",
    }
    

    return render(request,"products/view.html", context)

def sub_sub_catogary_product_view_by_color(request,slug, color):
    slug_type = request.build_absolute_uri().split('/')
    slug_type = slug_type[len(slug_type)-2]
    print(slug_type)
    try:
        sub_sub_cat_query = Sub_Sub_Category.objects.get(slug=slug)
    except Sub_Sub_Category.DoesNotExist:
        print("Product does not exist now!")
        return redirect("products:list")
    
    if sub_sub_cat_query is not None:
        queryset = Product_description.objects.filter(sub_sub_categary=sub_sub_cat_query, variation__title=color)
    else:
        queryset=Product_description.objects.all()
    context = {
          'qs': queryset ,
          'sub_slug': slug_type,
         "title":"Products",
    }
    

    return render(request,"products/view.html", context)



# def catogary_product_view_4(request):
    
#     query_4 = "Accessories"
    
#     print(query_4)
#     if query_4 is not None:
#         queryset = Product_description.objects.search(query_4)
#     else:
#         queryset=Product_description.objects.all()
#     context = {
#           'qs': queryset ,
#           'acessories_category': query_4,
#          "title":"Products",
#     }
    

#     return render(request,"products/view.html", context)


def catogary_product_view_1(request, slug,*args, **kwargs):
    
    try:
        cat_query = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        print("Product does not exist now!")
        return redirect("products:list")
    
    print(cat_query)
    
    if cat_query is not None:
        queryset = Product_description.objects.filter(categary=cat_query)
    else:
        queryset=Product_description.objects.all()
    context = {
          'qs': queryset ,
          
          #'clothing_category': query,
         "title":"Products",
    }
    # def get_context_data(self,*args, **kwargs):
    #     context=super(catogary_product_view ,self).get_context_data(*args, **kwargs)
    #     query=self.request.GET.get("query")
    #     context['query']=query
    #     #SearchQuery.objects.create(query=query)
    #     return context

    return render(request,"products/view.html", context)


def sub_catogary_product_view(request, slug,*args, **kwargs):
    
    try:
        sub_cat_query = Sub_Category.objects.get(slug=slug)
    except Sub_Category.DoesNotExist:
        print("Product does not exist now!")
        return redirect("products:list")
    
    print(sub_cat_query)
    slug_type = request.build_absolute_uri().split('/')
    slug_type = slug_type[len(slug_type)-2]
    print(slug_type)
    if sub_cat_query is not None:
        queryset = Product_description.objects.filter(sub_categary=sub_cat_query)
    else:
        queryset=Product_description.objects.all()
    context = {
          'qs': queryset ,
          'slug': slug_type,
          #'clothing_category': query,
         "title":"Products",
    }
    # def get_context_data(self,*args, **kwargs):
    #     context=super(catogary_product_view ,self).get_context_data(*args, **kwargs)
    #     query=self.request.GET.get("query")
    #     context['query']=query
    #     #SearchQuery.objects.create(query=query)
    #     return context

    return render(request,"products/view.html", context)


def sub_sub_catogary_product_view(request, slug,*args, **kwargs):
    
    try:
        sub_sub_cat_query = Sub_Sub_Category.objects.get(slug=slug)
    except Sub_Sub_Category.DoesNotExist:
        print("Product does not exist now!")
        return redirect("products:list")
    
    print(sub_sub_cat_query)
    slug_type = request.build_absolute_uri().split('/')
    slug_type = slug_type[len(slug_type)-2]
    print(slug_type)
    if sub_sub_cat_query is not None:
        queryset = Product_description.objects.filter(sub_sub_categary=sub_sub_cat_query)
    else:
        queryset=Product_description.objects.all()
    context = {
          'qs': queryset ,
          'sub_slug': slug_type,
          #'clothing_category': query,
         "title":"Products",
    }
    # def get_context_data(self,*args, **kwargs):
    #     context=super(catogary_product_view ,self).get_context_data(*args, **kwargs)
    #     query=self.request.GET.get("query")
    #     context['query']=query
    #     #SearchQuery.objects.create(query=query)
    #     return context

    return render(request,"products/view.html", context)






class SupplierHomeView(LoginRequiredMixin, DetailView):
    template_name = 'products/dashboard.html'
    def get_object(self):
        return self.request.user
    

class SupplierAddProductView(LoginRequiredMixin, DetailView):
    template_name = 'products/product_dashboard.html'
    def get_object(self):
        return self.request.user
    

class SupplierProductListView(LoginRequiredMixin,ListView):
    model = Product_description
    template_name='products/add_product_details.html'
    context_object_name = 'qs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['qs'] = Product_description.objects.filter(user = self.request.user)
        return context

class SupplierAddProductImageView(LoginRequiredMixin,CreateView):
    
    model = ProductImage
    form_class = ProductImageForm
    template_name = 'products/add_product_image.html'

    def form_valid(self,form):
        try:
            obj = form.save(commit=False)
            id = self.kwargs.get('id')
            obj.product = Product_description.objects.get(id=id)
            obj.save()
            return HttpResponseRedirect(self.get_success_url())
        except ObjectDoesNotExist:
            messages.warning(self.request, "your product does not exist.")
            return redirect("addproduct")

    
    def get_success_url(self):
        messages.success(self.request, 'Image added Successfully now add more details for your product !!!')
        return reverse("addproduct")

class SupplierAddProductVariationsView(LoginRequiredMixin,CreateView):
    
    model = Variation
    form_class = ProductVariationForm
    template_name = 'products/add_product_variations.html'

    def form_valid(self,form):
        try:
            obj = form.save(commit=False)
            id = self.kwargs.get('id')
            obj.product = Product_description.objects.get(id=id)
            obj.save()
            return HttpResponseRedirect(self.get_success_url())
        except ObjectDoesNotExist:
            messages.warning(self.request, "your product does not exist.")
            return redirect("addproduct")

    
    def get_success_url(self):
        messages.success(self.request, 'Variations added Successfully now add more details for your product !!!')
        return reverse("productquantity")   

class SupplierAddProductQuantityView(LoginRequiredMixin,CreateView):
    
    model = Quantity
    form_class = ProductQuantityForm
    template_name = 'products/add_product_variations.html'

    def form_valid(self,form):
        try:
            obj = form.save(commit=False)
            id = self.kwargs.get('id')
            obj.product = Product_description.objects.get(id=id)
            obj.save()
            return HttpResponseRedirect(self.get_success_url())
        except ObjectDoesNotExist:
            messages.warning(self.request, "your product does not exist.")
            return redirect("addproduct")

    
    def get_success_url(self):
        messages.success(self.request, 'Variations added Successfully now add more details for your product !!!')
        return reverse("addproduct")        




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
        messages.success(self.request, 'added Successfully now add more details for your product !!!')
        return reverse("addproduct")

        
        
    
    
    
    


class my_productsView(LoginRequiredMixin,ListView):
    model = Product_description
    template_name='products/my_products.html'
    context_object_name = 'qs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['qs'] = Product_description.objects.filter(user = self.request.user)
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