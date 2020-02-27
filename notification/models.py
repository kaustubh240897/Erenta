from django.db import models
#from django.contrib.auth.models import User
# Create your models here.
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order
from billing.models import BillingProfile,Charge
from carts.models import Cart,Quantity
from products.models import Product_description
User = settings.AUTH_USER_MODEL

class Notification(models.Model):
    title = models.CharField(max_length=256)
    message = models.TextField()
    viewed = models.BooleanField(default=False)
    user = models.ForeignKey(User,null=True,blank=True, on_delete=models.CASCADE)
    timestamp= models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=User)
def create_welcome_message(sender, **kwargs):
    if kwargs.get('created', False):
        Notification.objects.create(user = kwargs.get('instance'),
                                     title ="Welcome to eRenta!",
                                     message = "Thanks for registering.")





class Order_Notification(models.Model):
    title = models.CharField(max_length=256)
    message = models.TextField()
    viewed = models.BooleanField(default=False)
    billing_profile = models.ForeignKey(BillingProfile,null=True,blank=True, on_delete=models.CASCADE)
    timestamp= models.DateTimeField(auto_now_add=True)



@receiver(post_save, sender=Order)
def create_paid_order_msg(sender,instance,created, **kwargs):
    if created:
        Order_Notification.objects.create(billing_profile= instance.billing_profile,
                                title = "Order has been created",
                                message = "Dear User Thanks for being here.")

    


@receiver(post_save, sender=Charge)
def create_paid_ordersuccess_msg(sender,instance,created, **kwargs):
    if created:
        Order_Notification.objects.create(billing_profile= instance.billing_profile,
                                title = "Order has been Paid Successfully",
                                message = "Dear User Thanks for being here.")






class Supplier_Order_Notification(models.Model):
    title = models.CharField(max_length=256)
    message = models.TextField()
    viewed = models.BooleanField(default=False)
    status = models.CharField(max_length=120, default='created')
    order_id  = models.CharField( max_length=120, blank=True)
    cart   = models.ForeignKey(Cart,null=True,blank=True, on_delete=models.CASCADE)
    billing_profile = models.ForeignKey(BillingProfile,null=True,blank=True, on_delete=models.CASCADE)
    timestamp= models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=Order)
def receive_paid_ordersuccess_msg(sender,instance,created, **kwargs):
    Supplier_Order_Notification.objects.get_or_create(billing_profile = instance.billing_profile,
                                status = instance.status,
                                order_id = instance.order_id,
                                cart = instance.cart,
                                title = "you got an order",
                                message = "Dear User Thanks for being here.")

class Low_Quantity_Notification(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    viewed = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(Product_description,on_delete=models.CASCADE)
    timestamp= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s has only %s left" %(self.product, self.quantity)


@receiver(post_save, sender=Quantity)
def receive_paid_ordersuccess_msg(sender,instance,created, **kwargs):
    if int(instance.quantity) <= 3:
        Low_Quantity_Notification.objects.create(quantity=instance.quantity,
                                        product = instance.product,
                                        title = ("your product %s's quantity is low" %(instance.product)),
                                        message = "Add the quantity")



