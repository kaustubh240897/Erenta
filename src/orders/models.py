from django.db import models
from carts.models import Cart
# Create your models here.
ORDER_STATUS_CHOICES = (
    ('created','Created'),
    ('paid', 'Paid'),
    ('shipped','Shipped'),
    ('refunded','Refunded'),
)


class Order(models.Model):
    order_id = models.CharField( max_length=120, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, default='created')
    shipping_total = models.DecimalField(default=15.00,max_digits=50,decimal_places=2)
    total = models.DecimalField(default=0.00,max_digits=50,decimal_places=2)

    def __str__(self):
        return self.order_id

