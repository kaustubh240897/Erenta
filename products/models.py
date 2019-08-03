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
MY_CHOICES = ((1, 'S'),
               (2, 'M'),
               (3, 'L'),
               (4, 'XL'),
               (5, 'Not applicable'))


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
        lookups = Q(product_name__icontains=query) | Q(description__icontains=query) |Q(brand__icontains=query)|Q(registered_email=query)| Q(categary__icontains=query) | Q(cost_per_day__icontains=query) | Q(tag__product_name__icontains=query)
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

    
    
    

    


CATEGARY = (
    (('Clothing'), ('Clothing')),
    (('Accessories'), ('Accessories')),
    (('Books + novels'), ('Books + novels')),
    (('Instruments'), ('Instruments'))
)


class Product_description(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product_name = models.CharField(max_length=100)
    categary = models.CharField(choices=CATEGARY, default=1, max_length=50)
    sub_categary = models.CharField(max_length=50,default=None,null=True)
    description = models.TextField()
    quantity = models.IntegerField(default=1) 
    cost_per_day = models.DecimalField(max_digits=15, decimal_places=2 , null=True)
    size = MultiSelectField(choices=MY_CHOICES,default=5)
    #days = models.IntegerField( null=True, blank=True)
    brand = models.CharField(max_length=20, default=None,null=True)
    registered_email = models.EmailField(null=True)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    slug = models.SlugField(blank=True, unique=True)
    active = models.BooleanField(default=True)
    timestamp= models.DateTimeField(auto_now_add=True)


    objects = ProductManager()
    

    def get_absolute_url(self):
        #return "/products/{slug}/".format(slug=self.slug)
        return reverse ("products:detail", kwargs={"slug":self.slug})
    
    def get_absolute_url1(self):
        return reverse("update",kwargs={"slug":self.slug})


    def __str__(self):
        return self.product_name
    
    


    @property
    def name(self):
        return self.product_name

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug= unique_slug_generator(instance)
pre_save.connect(product_pre_save_receiver, sender=Product_description)



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
        
