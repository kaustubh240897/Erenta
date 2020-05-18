from django.db import models
#from django.contrib.auth.models import User
# Create your models here.
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order
from billing.models import BillingProfile,Charge
from carts.models import Cart,Quantity,CartItem
from products.models import Product_description,Variation
User = settings.AUTH_USER_MODEL




class Notification(models.Model):
    title = models.CharField(max_length=256)
    message = models.TextField()
    seen   = models.BooleanField(default=False)
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
    seen   = models.BooleanField(default=False)
    viewed = models.BooleanField(default=False)
    status = models.CharField(max_length=120, default='created')
    order_id  = models.CharField( max_length=120, blank=True)
    cart               = models.ForeignKey(Cart, on_delete=models.CASCADE)
    billing_profile = models.ForeignKey(BillingProfile,null=True,blank=True, on_delete=models.CASCADE)
    timestamp= models.DateTimeField(auto_now_add=True)



@receiver(post_save, sender=Order)
def create_paid_order_msg(sender,instance,created, **kwargs):
    if created:
        Order_Notification.objects.create(billing_profile= instance.billing_profile,
                                status = instance.status,
                                order_id = instance.order_id,
                                cart = instance.cart,
                                title = "Order has been created",
                                message = "Dear User Thanks for being here."
        )

    


@receiver(post_save, sender=Order)
def create_paid_ordersuccess_msg(sender,instance,created, **kwargs):
    if instance.status == 'paid':
        Order_Notification.objects.create(billing_profile= instance.billing_profile,
                                status = instance.status,
                                order_id = instance.order_id,
                                cart = instance.cart,
                                title = "Order has been Paid Successfully",
                                message = "Dear User Thanks for being here.")







class Supplier_Order_Notification(models.Model):
    title = models.CharField(max_length=256)
    message = models.TextField()
    viewed = models.BooleanField(default=False)
    seen   = models.BooleanField(default=False)
    status = models.CharField(max_length=120, default='created')
    order_id  = models.CharField( max_length=120, blank=True)
    cart               = models.ForeignKey(Cart, on_delete=models.CASCADE)
    billing_profile = models.ForeignKey(BillingProfile,null=True,blank=True, on_delete=models.CASCADE)
    timestamp= models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=Order)
def receive_paid_ordersuccess_msg(sender,instance,created, **kwargs):
    if instance.status == 'paid':
        Supplier_Order_Notification.objects.get_or_create(billing_profile = instance.billing_profile,
                                status = instance.status,
                                order_id = instance.order_id,
                                cart = instance.cart,
                                title = "you got an order",
                                message = "Dear User Thanks for being here.")



class Order_current_status(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    cart   = models.ForeignKey(Cart, on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)
    supplier_viewed = models.BooleanField(default=False)
    seen   = models.BooleanField(default=False)
    supplier_seen = models.BooleanField(default=False)
    product = models.ForeignKey(Product_description,null=True,blank=True,on_delete=models.CASCADE)
    status     = models.CharField(max_length=50, default='paid')
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=CartItem)
def Item_order_status_msg(sender,instance,created, **kwargs):
    if instance.status == 'shipped' or instance.status == 'returned back' or instance.status == 'refund requested' or  instance.refund_granted == True  or instance.status == 'cancellation request' or instance.cancel_granted == True:
        Order_current_status.objects.create(user = instance.cart.user,
                                status = instance.status,
                                cart = instance.cart,
                                product = instance.product,
                                
        )