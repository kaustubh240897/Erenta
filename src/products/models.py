from django.db.models import Q
import random
import os
from django.db import models
from django.db.models.signals import pre_save,post_save
from .utils import unique_slug_generator
from django.urls import reverse

# Create your models here.
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
        lookups = Q(product_name__icontains=query) | Q(description__icontains=query) | Q(cost_per_day__icontains=query)
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

class Product_description(models.Model):
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.CharField(max_length=10, default=1) 
    cost_per_day = models.DecimalField(max_digits=15, decimal_places=2 , null=True)
    days = models.IntegerField( null=True)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    slug = models.SlugField(blank=True, unique=True)
    active = models.BooleanField(default=True)
    timestamp= models.DateTimeField(auto_now_add=True)

    objects = ProductManager()

    def get_absolute_url(self):
        #return "/products/{slug}/".format(slug=self.slug)
        return reverse ("products:detail", kwargs={"slug":self.slug})

    def __str__(self):
        return self.product_name

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug= unique_slug_generator(instance)
pre_save.connect(product_pre_save_receiver, sender=Product_description)







