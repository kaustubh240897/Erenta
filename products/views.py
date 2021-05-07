from django.views.generic import ListView,DetailView,View,CreateView,FormView
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect ,get_object_or_404
from .models import Product_description,User_Review,Supplier_Review,ProductImage,Category,Sub_Category,Sub_Sub_Category,ProductImage,Variation,Product_Refund,RentalPeriod
from carts.models import Quantity,CartItem
from tags.models import Tag
from analytics.models import View_Count
#from accounts.forms import SupplierpersonaldetailForm, SupplierbankdetailForm
from accounts.models import User,Supplier,Bank_Account_Detail
from django.urls import reverse
from analytics.mixins import ObjectViewedMixin
from carts.models import Cart
import datetime
from datetime import date, timedelta
from .forms import ProductForm,ProductDetailChangeForm,RatingForm,SupplierRatingForm,ProductImageForm,ProductVariationForm,ProductQuantityForm,ProductImageChangeForm,ProductQuantityChangeForm,ProductTagForm,ProductRefundForm
from django.http import Http404
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import User
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
User = settings.AUTH_USER_MODEL

# Create your views here.
def product_list_view(request):
    if request.session.get('city_names',None) == None:
        request.session['city_names'] = "Tokyo"
    queryset = Product_description.objects.filter(Current_City__iexact=request.session['city_names'], active=True).order_by('?')
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
        'trending': View_Count.objects.filter(product__Current_City__iexact=request.session['city_names'], active=True)[:7]
        
    }
    return render(request,"products/product_list.html", context)


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
        if(self.request.user.is_authenticated == True):
            cart_obj = Cart.objects.filter(user=self.request.user).last()
            if cart_obj:
                self.request.session['cart_items']=cart_obj.cartitem_set.count()
            else:
                self.request.session['cart_items'] = 0
        else:
            cart_id = self.request.session.get("cart_id", None)
            if cart_id == None:
                self.request.session['cart_items'] = 0
            else:
                cart_obj, new_obj = Cart.objects.get_or_create(id=cart_id)
                if new_obj:
                    self.request.session['cart_items'] = 0
                else:
                    self.request.session['cart_items']=cart_obj.cartitem_set.count()


        slug = self.kwargs.get('slug')
        product= Product_description.objects.get(slug=slug)
        product_id = Product_description.objects.get(slug=slug)
        # context['form'] = OtherDetailForm(initial={'post': self.object })
        context['title'] = 'Details'
        context['qs1']=Variation.objects.filter(product__slug= slug)
        rentperiods =  RentalPeriod.objects.filter(product_name__slug=slug)
        rent_periods_list = []
        for obj in rentperiods:
            day = obj.start_date.day
            month = obj.start_date.month
            year = obj.start_date.year
            day1 = obj.end_date.day
            month1 = obj.end_date.month
            year1 = obj.end_date.year
            sdate = date(year, month, day)   # start date
            edate = date(year1, month1, day1)
            delta = edate - sdate       # as timedelta
            for i in range(delta.days + 1):
                day = sdate + timedelta(days=i)
                # print(day.strftime("%d/%m/%Y"))
                rent_periods_list.append(day.strftime("%d-%m-%Y"))
        context['rent_periods_list'] = rent_periods_list
        context['today_date'] = datetime.datetime.now().strftime('%d-%m-%Y')      
        #context['product_time']=Product_description.objects.filter(slug=slug, timestamp__gte=datetime.datetime.now() - datetime.timedelta(hours=744))
        context['qs'] = Quantity.objects.filter(product__slug = slug)
        context['all']=Product_description.objects.filter(Current_City__iexact= self.request.session['city_names'], slug=slug)
        context['similar_products']= View_Count.objects.filter(product__Current_City__iexact= self.request.session['city_names'], product__sub_category=product.sub_category).exclude(product__slug=slug)[:8]
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


        context['images']= qq
        context['reviews']=User_Review.objects.filter(product_id=product_id)
        return context
    
    

    def get_success_url(self):
        messages.success(self.request, 'added Successfully !!!')
        return reverse("products:detail",slug=self.kwargs.get('slug'))
    

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        if self.request.session.get('city_names',None) == None:
            self.request.session['city_names'] = "Tokyo"

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

# def sort_product_view_increase(self,category,request):
#     category = self.request.get(category)
#     category= Product_description.objects.get(category=category)
#     queryset1 = Product_description.objects.filter(category=category).order_by('cost_per_day')
    
#     context = {
#           'qs1': queryset1 ,
#          "title":"Sorted Products",
#     }
    

#     return render(request,"products/view.html", context)


# catogaries






def sub_category_product_view_by_color(request,slug, color):
    if request.session.get('city_names',None) == None:
        request.session['city_names'] = "Tokyo"
    
    slug_type = request.build_absolute_uri().split('/')
    slug_type = slug_type[len(slug_type)-2]
    print(slug_type)
    try:
        sub_cat_query = Sub_Category.objects.get(slug=slug)
    except Sub_Category.DoesNotExist:
        print("Product does not exist now!")
        return redirect("products:list")
    
    if sub_cat_query is not None:
        queryset = Product_description.objects.filter(Current_City__iexact=request.session['city_names'], sub_category=sub_cat_query, variation__title__icontains=color)
    else:
        queryset=Product_description.objects.filter(Current_City__iexact=request.session['city_names'])
    context = {
          'qs': queryset ,
          'slug': slug_type,
         "title":"Products",
         'trending': View_Count.objects.filter(product__Current_City__iexact=request.session['city_names'])[:7]
    }
    

    return render(request,"products/view.html", context)

def sub_sub_category_product_view_by_color(request,slug, color):
    if request.session.get('city_names',None) == None:
        request.session['city_names'] = "Tokyo"
    slug_type = request.build_absolute_uri().split('/')
    slug_type = slug_type[len(slug_type)-2]
    print(slug_type)
    try:
        sub_sub_cat_query = Sub_Sub_Category.objects.get(slug=slug)
    except Sub_Sub_Category.DoesNotExist:
        print("Product does not exist now!")
        return redirect("products:list")
    
    if sub_sub_cat_query is not None:
        queryset = Product_description.objects.filter(Current_City__iexact=request.session['city_names'],sub_sub_category=sub_sub_cat_query, variation__title__icontains=color)
    else:
        queryset=Product_description.objects.filter(Current_City__iexact=request.session['city_names'])
    context = {
          'qs': queryset ,
          'sub_slug': slug_type,
         "title":"Products",
         'trending': View_Count.objects.filter(product__Current_City__iexact=request.session['city_names'])[:7]
    }
    

    return render(request,"products/view.html", context)



# def category_product_view_4(request):
    
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


def category_product_view_1(request, slug,*args, **kwargs):
    if request.session.get('city_names',None) == None:
        request.session['city_names'] = "Tokyo"
    
    try:
        cat_query = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        print("Product does not exist now!")
        return redirect("products:list")
    
    print(cat_query)
    slug_type = request.build_absolute_uri().split('/')
    slug_type = slug_type[len(slug_type)-2]
    
    if cat_query is not None:
        queryset = Product_description.objects.filter(Current_City__iexact=request.session['city_names'], category=cat_query)
    else:
        queryset=Product_description.objects.filter(Current_City__iexact=request.session['city_names'])
    context = {
          'qs': queryset ,
          
         'cat_slug': slug_type,
         "title":"Products",
         'trending': View_Count.objects.filter(product__Current_City__iexact=request.session['city_names'])[:7]
    }
    # def get_context_data(self,*args, **kwargs):
    #     context=super(category_product_view ,self).get_context_data(*args, **kwargs)
    #     query=self.request.GET.get("query")
    #     context['query']=query
    #     #SearchQuery.objects.create(query=query)
    #     return context

    return render(request,"products/view.html", context)


def sub_category_product_view(request, slug,*args, **kwargs):
    if request.session.get('city_names',None) == None:
        request.session['city_names'] = "Tokyo"
    
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
        queryset = Product_description.objects.filter(Current_City__iexact=request.session['city_names'],sub_category=sub_cat_query)
    else:
        queryset=Product_description.objects.filter(Current_City__iexact=request.session['city_names'])
    context = {
          'qs': queryset ,
          'slug': slug_type,
          #'clothing_category': query,
         "title":"Products",
         'trending': View_Count.objects.filter(product__Current_City__iexact=request.session['city_names'])[:7]
    }
    # def get_context_data(self,*args, **kwargs):
    #     context=super(category_product_view ,self).get_context_data(*args, **kwargs)
    #     query=self.request.GET.get("query")
    #     context['query']=query
    #     #SearchQuery.objects.create(query=query)
    #     return context

    return render(request,"products/view.html", context)


def sub_sub_category_product_view(request, slug,*args, **kwargs):
    if request.session.get('city_names',None) == None:
        request.session['city_names'] = "Tokyo"
    
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
        queryset = Product_description.objects.filter(Current_City__iexact=request.session['city_names'], sub_sub_category=sub_sub_cat_query)
    else:
        queryset=Product_description.objects.filter(Current_City__iexact=request.session['city_names'])
    context = {
          'qs': queryset ,
          'sub_slug': slug_type,
          #'clothing_category': query,
         "title":"Products",
         'trending': View_Count.objects.filter(product__Current_City__iexact=request.session['city_names'])[:7]
    }
    # def get_context_data(self,*args, **kwargs):
    #     context=super(category_product_view ,self).get_context_data(*args, **kwargs)
    #     query=self.request.GET.get("query")
    #     context['query']=query
    #     #SearchQuery.objects.create(query=query)
    #     return context

    return render(request,"products/view.html", context)






class SupplierHomeView(LoginRequiredMixin, DetailView):
    template_name = 'products/dashboard.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SupplierHomeView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Supplier dashboard'
        
        return context
    
    def get_object(self):
        return self.request.user
    

# class SupplierAddProductView(LoginRequiredMixin, DetailView):
#     template_name = 'products/product_dashboard.html'
#     def get_object(self):
#         return self.request.user
    

class SupplierProductListView(LoginRequiredMixin,CreateView):
    model = Product_description
    form_class = ProductForm
    template_name = 'products/add_product_details.html'
    def form_valid(self,form):
        obj = form.save(commit=False)
        if Supplier.objects.filter(email=self.request.user).count()==0:
            return HttpResponseRedirect(self.get_success_url1())
        elif Bank_Account_Detail.objects.filter(email=self.request.user).count()==0:
            return HttpResponseRedirect(self.get_success_url2())
        else:
            obj.user = self.request.user # logged in user is available on a view func's `request` instance
            #obj.supplier = self.request.user 
            obj.save()
            
            return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['qs'] = Product_description.objects.filter(user = self.request.user).order_by('-timestamp')
        return context

    def get_success_url(self):
        messages.success(self.request, 'added Successfully now add more details for your product !!!')
        return reverse("addproductdetails")
    
    def get_success_url1(self):
        messages.success(self.request, 'Please add your personal details first !!!')
        return reverse("addsupplierpersonaldetail")
    
    def get_success_url2(self):
        messages.success(self.request, 'Please add your bank details first !!!')
        return reverse("addsupplierbankdetail")

        
    

    

class SupplierAddProductImageView(LoginRequiredMixin,CreateView):
    
    model = ProductImage
    form_class = ProductImageForm
    template_name = 'products/add_product_image.html'
    def get_context_data(self, *args, **kwargs):
        context = super(SupplierAddProductImageView, self).get_context_data(*args, **kwargs)
        id = self.kwargs.get('id')
        context['name'] = Product_description.objects.get(id=id)
        context['product_images'] = ProductImage.objects.filter(product__id=id)
        return context

    def form_valid(self,form):
        try:
            obj = form.save(commit=False)
            id = self.kwargs.get('id')
            obj.product = Product_description.objects.get(id=id)
            if Product_description.objects.filter(id=id,user=self.request.user).count()>0:
                if ProductImage.objects.filter(product__id=id).count() < 3:
                    obj.save()
                    return HttpResponseRedirect(self.get_success_url())
                else:
                    messages.warning(self.request, "You cannot add more than 3 images.")
                    return redirect("addproductdetails")
            else:
                messages.warning(self.request, "You are not authorized to add the image.")
                return redirect("addproductdetails")

            
        except ObjectDoesNotExist:
            messages.warning(self.request, "your product does not exist.")
            return redirect("addproductdetails")

    
    def get_success_url(self):
        messages.success(self.request, 'Image added Successfully now add more details for your product !!!')
        return reverse("productimage", kwargs={'id': self.kwargs.get('id')})

def remove_image(request,id1,id):
    try:
        obj = ProductImage.objects.get(id=id1)
        obj.delete()
        messages.success(request, 'removed Successfully !!!')
        return HttpResponseRedirect(reverse("productimage", args=(id,)))
    except ObjectDoesNotExist:
            messages.warning(self.request, "your product does not exist.")
            return redirect("addproductdetails")

class SupplierRentalPeriodView(LoginRequiredMixin,CreateView):
    
    model = RentalPeriod
    #form_class = RentalPeriodForm
    fields = '__all__'
    template_name = 'products/rental_period.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SupplierRentalPeriodView, self).get_context_data(*args, **kwargs)
        id = self.kwargs.get('id')
        context['rentperiod'] = "rentperiod" 
        context['name'] = Product_description.objects.get(id=id)
        context['rental_periods'] = RentalPeriod.objects.filter(product_name__id=id)
        return context

    def form_valid(self,form):
        try:
            obj = form.save(commit=False)
            id = self.kwargs.get('id')
            obj.product_name = Product_description.objects.get(id=id)
            if Product_description.objects.filter(id=id,user=self.request.user).count()>0:
                if RentalPeriod.objects.filter(product_name__id=id).count() < 10:
                    obj.save()
                    return HttpResponseRedirect(self.get_success_url())
                else:
                    messages.warning(self.request, "Sorry, You can not add more periods limit exceeded.")
                    return redirect("addproductdetails")
            else:
                messages.warning(self.request, "You are not authorized to add the rental period.")
                return redirect("addproductdetails")

        except ObjectDoesNotExist:
            messages.warning(self.request, "your product does not exist.")
            return redirect("addproductdetails")

    

    def get_success_url(self):
        messages.success(self.request, 'Rental period added Successfully now, you can add more periods for your product again !!!')
        return reverse("productrentalperiods", kwargs={'id': self.kwargs.get('id')})

def remove_rentalperiod(request,id1,id):
    try:
        obj = RentalPeriod.objects.get(id=id1)
        obj.delete()
        messages.success(request, 'removed Successfully !!!')
        return HttpResponseRedirect(reverse("productrentalperiods", args=(id,)))
    except ObjectDoesNotExist:
            messages.warning(self.request, "your product does not exist.")
            return redirect("addproductdetails")

class SupplierTagView(LoginRequiredMixin,CreateView):
    
    model = Tag
    form_class = ProductTagForm
    template_name = 'products/add_product_image.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SupplierTagView, self).get_context_data(*args, **kwargs)
        id = self.kwargs.get('id')
        context['alag'] = "alag" 
        context['name'] = Product_description.objects.get(id=id)
        context['tags'] = Tag.objects.filter(product_name__id=id)
        return context

    def form_valid(self,form):
        try:
            obj = form.save(commit=False)
            id = self.kwargs.get('id')
            obj.product_name = Product_description.objects.get(id=id)
            if Product_description.objects.filter(id=id,user=self.request.user).count()>0:
                if Tag.objects.filter(product_name__id=id).count() < 20:
                    obj.save()
                    return HttpResponseRedirect(self.get_success_url())
                else:
                    messages.warning(self.request, "Sorry, You can not add more tags limit exceeded.")
                    return redirect("addproductdetails")
            else:
                messages.warning(self.request, "You are not authorized to add the tags.")
                return redirect("addproductdetails")

        except ObjectDoesNotExist:
            messages.warning(self.request, "your product does not exist.")
            return redirect("addproductdetails")

    

    def get_success_url(self):
        messages.success(self.request, 'Tag added Successfully now, you can add more tags for your product again !!!')
        return reverse("producttags", kwargs={'id': self.kwargs.get('id')})

def remove_tags(request,id1,id):
    try:
        obj = Tag.objects.get(id=id1)
        obj.delete()
        messages.success(request, 'removed Successfully !!!')
        return HttpResponseRedirect(reverse("producttags", args=(id,)))
    except ObjectDoesNotExist:
            messages.warning(self.request, "your product does not exist.")
            return redirect("addproductdetails")


class SupplierAddProductVariationsView(LoginRequiredMixin,CreateView):
    
    model = Variation
    form_class = ProductVariationForm
    template_name = 'products/add_product_variations.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SupplierAddProductVariationsView, self).get_context_data(*args, **kwargs)
        id = self.kwargs.get('id')
        context['name'] = Product_description.objects.get(id=id)
        context['qs1']=Variation.objects.filter(product__id= id)
        return context

    def form_valid(self,form):
        try:
            obj = form.save(commit=False)
            id = self.kwargs.get('id')
            obj.product = Product_description.objects.get(id=id)
            if Product_description.objects.filter(id=id,user=self.request.user).count()>0:
                if Variation.objects.filter(product__id=id).count() < 25:
                    if Variation.objects.filter(product__id=id,category__iexact=self.request.POST['category'],title__iexact=self.request.POST['title']).count()==0:
                        obj.save()
                        return HttpResponseRedirect(self.get_success_url())
                    else:
                        messages.warning(self.request, "This category of product already exists.")
                        return redirect("addproductdetails")
                else:
                    messages.warning(self.request, " Sorry!, You had crossed the limit for adding variations for a item.")
                    return redirect("addproductdetails")
            else:
                messages.warning(self.request, "You are not authorized to add the variations.")
                return redirect("addproductdetails")

        except ObjectDoesNotExist:
            messages.warning(self.request, "your product does not exist.")
            return redirect("addproductdetails")

    
    def get_success_url(self):
        messages.success(self.request, 'Variations added Successfully, You can add more(unique) variations again !!!')
        return reverse("productvariations", kwargs={'id': self.kwargs.get('id')})

def remove_variations(request,id1,id):
    try:
        obj = Variation.objects.get(id=id1)
        obj1 = Quantity.objects.filter(product__id=id,variations__id = id1)
        obj.delete()
        for object1 in obj1:
            object1.delete()
        messages.success(request, 'removed Successfully !!!')
        return HttpResponseRedirect(reverse("productvariations", args=(id,)))
    except ObjectDoesNotExist:
            messages.warning(self.request, "your product does not exist.")
            return redirect("addproductdetails")

class SupplierAddProductQuantityView(LoginRequiredMixin,CreateView):
    
    model = Quantity
    form_class = ProductQuantityForm
    template_name = 'products/add_product_quantity.html'
    def get_context_data(self, *args, **kwargs):
        context = super(SupplierAddProductQuantityView, self).get_context_data(*args, **kwargs)
        
        id = self.kwargs.get('id')
        product= Product_description.objects.get(id=id)
        context['name'] = Product_description.objects.get(id=id)
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
            if Product_description.objects.filter(id=id,user=self.request.user).count()>0:
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
                    

                    if self.request.POST.get('color',None) and self.request.POST.get('size',None):
                        if Quantity.objects.filter(product__id = id, variations__title__iexact = self.request.POST.get('color',None)).filter(product__id = id, variations__title__iexact = self.request.POST.get('size',None)).count()==0:
                            quantity_item= Quantity.objects.create(product=product_obj)
                            
                            if len(product_variations)>0:
                                obj.variation_set=quantity_item.variations.add(*product_variations)
                            quantity_item.quantity = qty
                            quantity_item.product = Product_description.objects.get(id=id)
                            quantity_item.save()
                            return HttpResponseRedirect(self.get_success_url())
                        else:
                            messages.warning(self.request,'Oops! You had already entered this item\'s (with same color and size *if applied) quantity, You can update it in myproduct section in dashboard.')
                            return redirect("addproductdetails")
                    elif self.request.POST.get('color',None) or self.request.POST.get('size',None):
                        if Quantity.objects.filter(product__id = id, variations__title__iexact = self.request.POST.get('color',None)).count() + Quantity.objects.filter(product__id = id, variations__title__iexact = self.request.POST.get('size',None)).count() == 0:
                            quantity_item= Quantity.objects.create(product=product_obj)
                            
                            if len(product_variations)>0:
                                print(product_variations)
                                obj.variation_set=quantity_item.variations.add(*product_variations)
                            quantity_item.quantity = qty
                            quantity_item.product = Product_description.objects.get(id=id)
                            quantity_item.save()
                            return HttpResponseRedirect(self.get_success_url())
                        else:
                            messages.warning(self.request, "OOps!  You had already entered this item\'s (with same color and size *if applied) quantity, You can update it in myproduct section in dashboard.")
                            return redirect("addproductdetails")
                    else:
                        if Quantity.objects.filter(product__id = id).count() == 0:
                            quantity_item= Quantity.objects.create(product=product_obj)
                            
                            if len(product_variations)>0:
                                obj.variation_set=quantity_item.variations.add(*product_variations)
                            quantity_item.quantity = qty
                            quantity_item.product = Product_description.objects.get(id=id)
                            quantity_item.save()
                            return HttpResponseRedirect(self.get_success_url())
                        else:
                            messages.warning(self.request, "OOps! You had already entered this item\'s (with same color and size *if applied) quantity, You can update it in myproduct section in dashboard.")
                            return redirect("addproductdetails")



                else:
                    messages.warning(self.request, "OOps! you entered wrong quantity.")
                    return redirect("addproductdetails")
            else:
                messages.warning(self.request, "You are not authorized to add the quantity.")
                return redirect("addproductdetails")


            #obj.save()
            
        except ObjectDoesNotExist:
            messages.warning(self.request, "your product does not exist.")
            return redirect("addproduct")

    
    def get_success_url(self):
        messages.success(self.request, 'Quantity added Successfully. !!!')
        return reverse("productquantity", kwargs={'id': self.kwargs.get('id')})      


def remove_quantity(request,id1,id):
    try:
        obj = Quantity.objects.get(id=id1)
        obj.delete()
        messages.success(request, 'removed Successfully !!!')
        return HttpResponseRedirect(reverse("productquantity", args=(id,)))
    except ObjectDoesNotExist:
            messages.warning(self.request, "your product does not exist.")
            return redirect("addproductdetails")


def load_sub_category(request):
    category_id = request.GET.get('category_id')
    sub_category = Sub_Category.objects.filter(category_id=category_id)
    return render(request, 'products/sub_category_dropdown_list_options.html', {'sub_category': sub_category})

def load_sub_sub_category(request):
    sub_category_id = request.GET.get('sub_category_id')
    sub_sub_category = Sub_Sub_Category.objects.filter(sub_category_id=sub_category_id)
    return render(request, 'products/sub_sub_category_dropdown_list_options.html', {'sub_sub_category': sub_sub_category})

# class AddProductView(LoginRequiredMixin,CreateView):
    
#     model = Product_description
#     form_class = ProductForm
#     template_name = 'products/add_products.html'
#     def form_valid(self,form):
#         obj = form.save(commit=False)
#         if Supplier.objects.filter(email=self.request.user).count()==0:
#             return HttpResponseRedirect(self.get_success_url1())
#         elif Bank_Account_Detail.objects.filter(email=self.request.user).count()==0:
#             return HttpResponseRedirect(self.get_success_url2())
#         else:
#             obj.user = self.request.user # logged in user is available on a view func's `request` instance
#             #obj.supplier = self.request.user 
#             obj.save()
            
#             return HttpResponseRedirect(self.get_success_url())


#     def get_success_url(self):
#         messages.success(self.request, 'added Successfully now add more details for your product !!!')
#         return reverse("addproductdetails")
    
#     def get_success_url1(self):
#         messages.success(self.request, 'Please add your personal details first !!!')
#         return reverse("addsupplierpersonaldetail")
    
#     def get_success_url2(self):
#         messages.success(self.request, 'Please add your bank details first !!!')
#         return reverse("addsupplierbankdetail")

        
        
    
    
    
    


class my_productsView(LoginRequiredMixin,ListView):
    model = Product_description
    template_name='products/my_products.html'
    context_object_name = 'qs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['qs'] = Product_description.objects.filter(user = self.request.user).order_by('-timestamp')
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
        slug = self.kwargs.get('slug')
        context['title']="Change product's details"
        context['name'] = Product_description.objects.get(slug=slug)
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'Updated Successfully !!!')
        return reverse("update" , kwargs={'slug': self.kwargs.get('slug')})


class my_productsimageView(LoginRequiredMixin,ListView):
    model = ProductImage
    template_name='products/my_product_images.html'
    context_object_name = 'qs'

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get('slug')
        context = super().get_context_data(**kwargs)
        context['qs'] = ProductImage.objects.filter(product__slug = slug)
        context['name'] = Product_description.objects.get(slug=slug)
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
        id = self.kwargs.get('id')
        context['title']='Update your product images'
        context['name'] = ProductImage.objects.get(id=id)
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'Updated Successfully !!!')
        return reverse("product:imageupdate" , kwargs={'id': self.kwargs.get('id')})



class my_productsquantityView(LoginRequiredMixin,ListView):
    model = Quantity
    template_name='products/my_product_quantity.html'
    context_object_name = 'qs'

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get('slug')
        context = super().get_context_data(**kwargs)
        context['qs1']=Variation.objects.filter(product__slug= slug)
        context['qs'] = Quantity.objects.filter(product__slug = slug)
        context['name'] = Product_description.objects.get(slug=slug)
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
        id = self.kwargs.get('id')
        context['title1']='Update your product quantity'
        context['name'] = Quantity.objects.get(id=id)
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'Updated Successfully !!!')
        return reverse("products:quantityupdate" , kwargs={'id': self.kwargs.get('id')})




class ReviewView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        id = self.kwargs.get('id')
        form = RatingForm()
        context={
            'form': form,
            'item' : CartItem.objects.get(id=id),
            'count' : User_Review.objects.filter(cartitem_id=id).count()
        }
        return render(self.request, "products/review.html" ,context)
    def post(self,*args, **kwargs):
        form = RatingForm(self.request.POST)
        if form.is_valid():
            slug = self.kwargs.get('slug')
            id = self.kwargs.get('id')
            rating = form.cleaned_data.get('rating')
            review   = form.cleaned_data.get('review')
            # edit the order
            try:
                product_id=Product_description.objects.get(slug=slug)
                product_id.save()
                #store the refund
                reviews = User_Review()
                reviews.product_id = product_id
                reviews.cartitem_id = id
                reviews.email = self.request.user
                reviews.rating = rating
                reviews.review  = review
                #reviews.reviewed = True
                reviews.save()
                messages.info(self.request, "Your review has received.")
                return redirect("orders:list")
            except ObjectDoesNotExist:
                messages.warning(self.request, "This product does not exist.")
                return redirect("orders:list")





class ProductRefundView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        id = self.kwargs.get('id')
        form = ProductRefundForm()
        context={
            'form': form,
            'product_refund': 'product_refund',
            'item': CartItem.objects.get(id=id),
            'count': Product_Refund.objects.filter(cartitem_id=id).count()
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
                product_item.status = 'refund requested'
                #product_item.line_total = None
                product_item.save()
                #store the refund
                reviews = Product_Refund()
                reviews.product_id = product_id
                reviews.cartitem_id = id
                reviews.email = self.request.user
                reviews.reason = reason
                reviews.save()
                messages.info(self.request, "Your refund request has been received.")
                return redirect("orders:list")
            except ObjectDoesNotExist:
                messages.warning(self.request, "This product does not exist.")
                return redirect("orders:list")





class SupplierReviewView(LoginRequiredMixin,View):
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