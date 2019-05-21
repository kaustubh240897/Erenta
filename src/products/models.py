from django.db import models

# Create your models here.
class Product_description(models.Model):
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.CharField(max_length=10, default=1) 
    cost = models.DecimalField(max_digits=15, decimal_places=2 , null=True)

    def __str__(self):
        return self.product_name






