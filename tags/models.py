from django.db import models
from django.db.models.signals import pre_save,post_save
from Ecommerce_Intern.utils import unique_slug_generator
from products.models import Product_description
from django.urls import reverse

# Create your models here.

class Tag(models.Model):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField()
    timestamp = models.DateTimeField(auto_now_add=True)
    active =models.BooleanField(default=True)
    products = models.ManyToManyField(Product_description, blank=True)
    

    def __str__(self):
        return self.product_name

def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug= unique_slug_generator(instance)
pre_save.connect(tag_pre_save_receiver, sender=Tag)





