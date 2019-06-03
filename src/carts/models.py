from django.conf import settings
from django.db import models

from products.models import Product_description

User = settings.AUTH_USER_MODEL

class CartManager(models.Manager):
    def new(self,user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated():
                user_obj=user_obj
            
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product_description,blank=True)
    total = models.DecimalField(default=0.00, max_digits=50, decimal_places=2 )
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)




