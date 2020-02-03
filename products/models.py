from django.db.models import Q
from django.conf import settings
import random
import os
from django.db import models
from multiselectfield import MultiSelectField
from django.db.models.signals import pre_save,post_save
from Ecommerce_Intern.utils import unique_slug_generator
from django.urls import reverse
#from django.contrib.auth import get_user_model

User = settings.AUTH_USER_MODEL

# Create your models here.
# MY_CHOICES = ((1, 'S'),
#                (2, 'M'),
#                (3, 'L'),
#                (4, 'XL'),
#                (5, 'Not applicable'))


def get_filename_ext(filepath):
    base_name=os.path.basename(filepath)
    name, ext=os.path.splitext(base_name)
    return name,ext


def upload_image_path(instance, filename):
    
    new_filename=random.randint(1,399900000)
    name,ext=get_filename_ext(filename)
    final_filename='{new_filename} {ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
        )

class ProductQuerySet(models.query.QuerySet):
    def active(self):
       return self.filter(active=True)

    def search(self, query):
        lookups = Q(product_name__icontains=query)| Q(variation__title__icontains=query) | Q(description__icontains=query) |Q(brand__icontains=query) | Q(categary__icontains=query) | Q(cost_per_day__icontains=query) | Q(tag__product_name__icontains=query)
        return self.filter(lookups).distinct()



class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def get_by_slug(self, slug):
        qs = self.get_queryset().active().filter(slug=slug) # products_description.objects
        if qs.count()==1:
            return qs.first
        return None
    
    def search(self, query):
        return self.get_queryset().active().search(query)

    
    
    

    





class Category(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True)
    featured = models.BooleanField(default=None)
    active = models.BooleanField(default=True)
    timestamp= models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)
    
    # def get_absolute_url_cat(self):
    #     #return "/products/{slug}/".format(slug=self.slug)
    #     return reverse ("products:query", kwargs={"slug":self.slug})

    def __str__(self):
        return self.title
    

class Sub_Category(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True)
    featured = models.BooleanField(default=None)
    active = models.BooleanField(default=True)
    timestamp= models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)
    
    # def get_absolute_url_cat(self):
    #     #return "/products/{slug}/".format(slug=self.slug)
    #     return reverse ("products:query", kwargs={"slug":self.slug})

    def __str__(self):
        return self.title

class Sub_Sub_Category(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True)
    featured = models.BooleanField(default=None)
    active = models.BooleanField(default=True)
    timestamp= models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)
    
    # def get_absolute_url_cat(self):
    #     #return "/products/{slug}/".format(slug=self.slug)
    #     return reverse ("products:query", kwargs={"slug":self.slug})

    def __str__(self):
        return self.title

    


class Product_description(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product_name = models.CharField(max_length=100)
    categary = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True,null=True)
    sub_categary = models.ForeignKey(Sub_Category,on_delete=models.CASCADE,blank=True,null=True)
    sub_sub_categary = models.ForeignKey(Sub_Sub_Category,on_delete=models.CASCADE,blank=True,null=True) 
    description = models.TextField()
    #quantity = models.IntegerField(default=1) 
    cost_per_day = models.DecimalField(max_digits=15, decimal_places=2 , null=True)
    discount_price = models.DecimalField(max_digits=15, decimal_places=2,blank=True,null=True)
    #size = MultiSelectField(choices=MY_CHOICES,default=5)
    #days = models.IntegerField( null=True, blank=True)
    brand = models.CharField(max_length=20, default=None,null=True)
    #registered_email = models.EmailField(null=True)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    slug = models.SlugField(blank=True, unique=True)
    active = models.BooleanField(default=True)
    timestamp= models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)


    objects = ProductManager()
    

    def get_absolute_url(self):
        #return "/products/{slug}/".format(slug=self.slug)
        return reverse ("products:detail", kwargs={"slug":self.slug})
    
    def get_absolute_url1(self):
        return reverse("update",kwargs={"slug":self.slug})
    
    def get_amount_percent_saved(self):
        return format((((self.cost_per_day-self.discount_price)/(self.cost_per_day))*100),'.2f')

    def __str__(self):
        return self.product_name
    
    class Meta:
        unique_together=('product_name','slug') 


    @property
    def name(self):
        return self.product_name

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug= unique_slug_generator(instance)
pre_save.connect(product_pre_save_receiver, sender=Product_description)


class ProductImage(models.Model):
    product=models.ForeignKey(Product_description,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    thumbnail = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)

    def __str__(self):
        return self.product.product_name


class VariationManager(models.Manager):
    def all(self):
        return super(VariationManager, self).filter(active=True)
    def sizes(self):
        return self.all().filter(category='size')
    def colors(self):
        return self.all().filter(category='color')




VAR_CATEGORIES = (
    ('size','size'),
    ('color','color'),
    ('package','package'),

)

class Variation(models.Model):
    product = models.ForeignKey(Product_description,on_delete=models.CASCADE)
    category = models.CharField(max_length=120, choices=VAR_CATEGORIES,default='size')
    title = models.CharField(max_length=120)
    image = models.ForeignKey(ProductImage,null=True,blank=True,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=2 ,null=True,blank=True)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.title



class Contact(models.Model):
    msd_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70)
    subject = models.CharField(max_length=70)
    message = models.CharField(max_length=500)

    def __str__(self):
        return self.email


RATING = (
    (('1'), ('1')),
    (('2'), ('2')),
    (('3'), ('3')),
    (('4'), ('4')),
    (('5'), ('5'))
)


class User_Review(models.Model):
    product_id = models.ForeignKey(Product_description,on_delete=models.CASCADE)
    email     = models.ForeignKey(User,on_delete=models.CASCADE)
    rating    = models.CharField(choices=RATING, default=5, max_length=10)
    review = models.TextField()
    timestamp= models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.product_id}"
    

class Supplier_Review(models.Model):
    customer  = models.EmailField(default=None,null=True,blank=True)
    email     = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    rating    = models.CharField(choices=RATING, default=5, max_length=10)
    review = models.TextField()
    timestamp= models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return "%s reviewed on %s" %(self.email, self.timestamp)
        
