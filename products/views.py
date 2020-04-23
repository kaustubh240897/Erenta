from django.views.generic import ListView,DetailView,View,CreateView,FormView
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect ,get_object_or_404
from .models import Product_description,User_Review,Supplier_Review,ProductImage,Category,Sub_Category,Sub_Sub_Category,ProductImage,Variation,Product_Refund
from carts.models import Quantity,CartItem
from tags.models import Tag
from analytics.models import View_Count
#from accounts.forms import SupplierpersonaldetailForm, SupplierbankdetailForm
from accounts.models import User,Supplier,Bank_Account_Detail
from django.urls import reverse
from analytics.mixins import ObjectViewedMixin
from carts.models import Cart
from otherdetails.models import OtherDetails
from .forms import ProductForm,ProductDetailChangeForm,RatingForm,SupplierRatingForm,ProductImageForm,ProductVariationForm,ProductQuantityForm,ProductImageChangeForm,ProductQuantityChangeForm,ProductTagForm,ProductRefundForm
from django.http import Http404
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from carts.forms import OtherDetailForm
from accounts.models import User
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
User = settings.AUTH_USER_MODEL

# Create your views here.
def product_list_view(request):
    queryset = Product_description.objects.all().order_by('?')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 16)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {
        'qs': queryset ,
        "title":"Products",
        'products': products,
        'trending': View_Count.objects.all()[:5]
        
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
        views = request.user.objectviewed_set.by_model(Product_description, model_queryset=False).distinct()[:10]
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
        context['qs1']=Variation.objects.filter(product__slug= slug)
        context['qs'] = Quantity.objects.filter(product__slug = slug)
        context['all']=Product_description.objects.get(slug=slug)
        context['similar_products']= View_Count.objects.filter(product__sub_sub_categary=product.sub_sub_categary).exclude(product__slug=slug)[:8]
        qq = ProductImage.objects.filter(product=product)
        if qq.count()==3:
            context['images0'] = qq[0]
            context['images1'] = qq[1]
            context['images2'] = qq[2]
        elif qq.count()==2:
            context['images0'] = qq[0]
            context['images1'] = qq[1]
        elif qq.count()==1:
            context['images0'] = qq[0]


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

    # def get_context_data(self, *args, **kwargs):
    #     context = super(SupplierHomeView, self).get_context_data(*args, **kwargs)
    #     context['personal_details']=Supplier.objects.filter(email=self.request.user)
    #     context['form'] = SupplierpersonaldetailForm()
        
    #     return context
    
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
            if ProductImage.objects.filter(product__id=id).count() < 3:
                obj.save()
                return HttpResponseRedirect(self.get_success_url())
            else:
                messages.warning(self.request, "You cannot add more than 3 images.")
                return redirect("addproduct")
            
        except ObjectDoesNotExist:
            messages.warning(self.request, "your product does not exist.")
            return redirect("addproduct")

    
    def get_success_url(self):
        messages.success(self.request, 'Image added Successfully now add more details for your product !!!')
        return reverse("addproductdetails")


class SupplierTagView(LoginRequiredMixin,CreateView):
    
    model = Tag
    form_class = ProductTagForm
    template_name = 'products/add_product_image.html'

    def form_valid(self,form):
        try:
            obj = form.save(commit=False)
            id = self.kwargs.get('id')
            obj.product_name = Product_description.objects.get(id=id)
            obj.save()
            return HttpResponseRedirect(self.get_success_url())
        except ObjectDoesNotExist:
            messages.warning(self.request, "your product does not exist.")
            return redirect("addproduct")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['alag'] = "alag" 
        return context

    def get_success_url(self):
        messages.success(self.request, 'Tag added Successfully now, you can add more tags for your product again !!!')
        return reverse("addproductdetails")




class SupplierAddProductVariationsView(LoginRequiredMixin,CreateView):
    
    model = Variation
    form_class = ProductVariationForm
    template_name = 'products/add_product_variations.html'

    def form_valid(self,form):
        try:
            obj = form.save(commit=False)
            id = self.kwargs.get('id')
            obj.product = Product_description.objects.get(id=id)
            
            if Variation.objects.filter(product__id=id,category=self.request.POST['category'],title=self.request.POST['title']).count()==0:
                obj.save()
                return HttpResponseRedirect(self.get_success_url())
            else:
                messages.warning(self.request, "This category of product already exists.")
                return redirect("addproduct")

        except ObjectDoesNotExist:
            messages.warning(self.request, "your product does not exist.")
            return redirect("addproduct")

    
    def get_success_url(self):
        messages.success(self.request, 'Variations added Successfully, You can add more(unique) variations again !!!')
        return reverse("addproductdetails")   

class SupplierAddProductQuantityView(LoginRequiredMixin,CreateView):
    
    model = Quantity
    form_class = ProductQuantityForm
    template_name = 'products/add_product_quantity.html'
    def get_context_data(self, *args, **kwargs):
        context = super(SupplierAddProductQuantityView, self).get_context_data(*args, **kwargs)
        
        id = self.kwargs.get('id')
        product= Product_description.objects.get(id=id)
        
        context['title'] = 'Add Quantity Details'
        context['qs']=Quantity.objects.filter(product__id= id)
        context['object']=Variation.objects.filter(product=product)
        
        return context

    def form_valid(self,form):
        try:
            product_variations = []
            
            obj = form.save(commit=False)
            id = self.kwargs.get('id')
            qty = self.request.POST['qty']
            product_obj = Product_description.objects.get(id=id)
            #obj.product = Product_description.objects.get(id=id)
            if int(qty)>0:
                for item in self.request.POST:
                    key = item
                    val = self.request.POST[key]
                    try:
                        v = Variation.objects.get(product=product_obj, category__iexact=key, title__iexact=val)
                        product_variations.append(v)
                        print(v)
                    except:
                        pass
                #print("111111qqqqq",Quantity.objects.filter(product__id=id,variations__title__iexact=self.request.POST[key]).count())
                if Product_description.objects.get(id=id):
                    quantity_item= Quantity.objects.create(product=product_obj)
                    
                    if len(product_variations)>0:
                        obj.variation_set=quantity_item.variations.add(*product_variations)
                    quantity_item.quantity = qty
                    quantity_item.product = Product_description.objects.get(id=id)
                    quantity_item.save()
                    return HttpResponseRedirect(self.get_success_url())
                else:
                    messages.warning(self.request, "OOps! you already entered this item quantity.")
                    return redirect("addproductdetails")


            else:
                messages.warning(self.request, "OOps! you entered wrong quantity.")
                return redirect("addproductdetails")

            #obj.save()
            
        except ObjectDoesNotExist:
            messages.warning(self.request, "your product does not exist.")
            return redirect("addproduct")

    
    def get_success_url(self):
        messages.success(self.request, 'Quantity added Successfully. !!!')
        return reverse("addproductdetails")        




class AddProductView(LoginRequiredMixin,CreateView):
    
    model = Product_description
    form_class = ProductForm
    template_name = 'products/add_products.html'
    def form_valid(self,form):
        obj = form.save(commit=False)
        if Supplier.objects.filter(email=self.request.user).count()==0:
            return HttpResponseRedirect(self.get_success_url1())
        elif Bank_Account_Detail.objects.filter(email=self.request.user).count()==0:
            return HttpResponseRedirect(self.get_success_url2())
        else:
            obj.user = self.request.user # logged in user is available on a view func's `request` instance
            obj.save()
            return HttpResponseRedirect(self.get_success_url())


    def get_success_url(self):
        messages.success(self.request, 'added Successfully now add more details for your product !!!')
        return reverse("addproductdetails")
    
    def get_success_url1(self):
        messages.success(self.request, 'Please add your personal details first !!!')
        return reverse("addsupplierpersonaldetail")
    
    def get_success_url2(self):
        messages.success(self.request, 'Please add your bank details first !!!')
        return reverse("addsupplierbankdetail")

        
        
    
    
    
    


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


class my_productsimageView(LoginRequiredMixin,ListView):
    model = ProductImage
    template_name='products/my_product_images.html'
    context_object_name = 'qs'

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get('slug')
        context = super().get_context_data(**kwargs)
        context['qs'] = ProductImage.objects.filter(product__slug = slug)
        return context
       

class ProductImageUpdateView(LoginRequiredMixin,UpdateView):
    form_class = ProductImageChangeForm
    model = ProductImage
    template_name = 'products/product-update-image-view.html'
    

    def get_object(self, *args, **kwargs):
        request = self.request
        id = self.kwargs.get('id')

        #instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = ProductImage.objects.get(id=id, active=True)
        except ProductImage.DoesNotExist:
            raise Http404("Not found..")
        except ProductImage.MultipleObjectsReturned:
            qs = ProductImage.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Uhhmmm ")
        #object_viewed_signal.send(instance.__class__, instance-instance, request=request)
        return instance


    
    def get_context_data(self,*args,**kwargs):
        context = super(ProductImageUpdateView,self).get_context_data(*args,**kwargs)
        context['title']='Update your product images'
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'Updated Successfully !!!')
        return reverse("supplier")



class my_productsquantityView(LoginRequiredMixin,ListView):
    model = Quantity
    template_name='products/my_product_quantity.html'
    context_object_name = 'qs'

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get('slug')
        context = super().get_context_data(**kwargs)
        context['qs1']=Variation.objects.filter(product__slug= slug)
        context['qs'] = Quantity.objects.filter(product__slug = slug)
        return context

class ProductQuantityUpdateView(LoginRequiredMixin,UpdateView):
    form_class = ProductQuantityChangeForm
    model = Quantity
    template_name = 'products/product-update-image-view.html'
    

    def get_object(self, *args, **kwargs):
        request = self.request
        id = self.kwargs.get('id')

        #instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Quantity.objects.get(id=id, active=True)
        except Quantity.DoesNotExist:
            raise Http404("Not found..")
        except Quantity.MultipleObjectsReturned:
            qs = Quantity.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Uhhmmm ")
        #object_viewed_signal.send(instance.__class__, instance-instance, request=request)
        return instance


    
    def get_context_data(self,*args,**kwargs):
        context = super(ProductQuantityUpdateView,self).get_context_data(*args,**kwargs)
        # context['title']='Update your product images'
        context['title1']='Update your product quantity'
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
            slug = self.kwargs.get('slug')
            rating = form.cleaned_data.get('rating')
            review   = form.cleaned_data.get('review')
            # edit the order
            try:
                product_id=Product_description.objects.get(slug=slug)
                product_id.save()
                #store the refund
                reviews = User_Review()
                reviews.product_id = product_id
                reviews.email = self.request.user
                reviews.rating = rating
                reviews.review  = review
                reviews.save()
                messages.info(self.request, "Your review has received.")
                return redirect("orders:list")
            except ObjectDoesNotExist:
                messages.warning(self.request, "This product does not exist.")
                return redirect("orders:list")





class ProductRefundView(View):
    def get(self, *args, **kwargs):
        form = ProductRefundForm()
        context={
            'form': form
        }
        return render(self.request, "products/review.html" ,context)
    def post(self,*args, **kwargs):
        form = ProductRefundForm(self.request.POST)
        if form.is_valid():
            slug = self.kwargs.get('slug')
            id = self.kwargs.get('id')
            reason = form.cleaned_data.get('reason')
            
            # edit the order
            try:
                product_id=Product_description.objects.get(slug=slug)
                product_id.save()
                product_item=CartItem.objects.get(id=id)
                #order.status = refunded
                product_item.refund_requested = True
                #product_item.line_total = None
                product_item.save()
                #store the refund
                reviews = Product_Refund()
                reviews.product_id = product_id
                reviews.email = self.request.user
                reviews.reason = reason
                reviews.save()
                messages.info(self.request, "Your refund request has been received.")
                return redirect("orders:list")
            except ObjectDoesNotExist:
                messages.warning(self.request, "This product does not exist.")
                return redirect("orders:list")





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