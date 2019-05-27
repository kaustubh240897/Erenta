import random
import os
from django.db import models

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


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id) # products_description.objects
        if qs.count()==1:
            return qs.first
        return None

class Product_description(models.Model):
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.CharField(max_length=10, default=1) 
    cost_per_day = models.DecimalField(max_digits=15, decimal_places=2 , null=True)
    days = models.IntegerField( null=True)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    active = models.BooleanField(default=True)

    objects = ProductManager()

    def __str__(self):
        return self.product_name






