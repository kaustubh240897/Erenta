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


class Product_description(models.Model):
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.CharField(max_length=10, default=1) 
    cost = models.DecimalField(max_digits=15, decimal_places=2 , null=True)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)

    def __str__(self):
        return self.product_name






