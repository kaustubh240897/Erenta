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
from django.core.mail import send_mail
User = settings.AUTH_USER_MODEL




class Notification(models.Model):
    title = models.CharField(max_length=256)
    message = models.TextField()
    seen   = models.BooleanField(default=False)
    viewed = models.BooleanField(default=False)
    user = models.ForeignKey(User,null=True,blank=True, on_delete=models.CASCADE)
    timestamp= models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=User)
def create_welcome_message(sender,instance, **kwargs):
    if kwargs.get('created', False):
        Notification.objects.create(user = kwargs.get('instance'),
                                     title ="Welcome to eRenta!",
                                     message = "Thanks for registering.")
        send_mail('Welcome to eRenta!', 'Thanks for registering on Erenta', 'erentajapan@gmail.com', [instance.email,])





class Order_Notification(models.Model):
    title = models.CharField(max_length=256)
    message = models.TextField()
    seen   = models.BooleanField(default=False)
    viewed = models.BooleanField(default=False)
    status = models.CharField(max_length=120, default='created')
    order_id  = models.CharField( max_length=120, blank=True)
    cart               = models.ForeignKey(Cart,null=True, blank=True, on_delete=models.CASCADE)
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
        send_mail('Erenta:Your Order has been Paid Successfully', 'Dear User, Your Order has been Paid Successfully. Thanks for being here.', 'erentajapan@gmail.com', [instance.billing_profile.email,])




# class User_Order_Status_Notification(models.Model):
#     product = models.ForeignKey(Product_description, null=True,blank=True,on_delete=models.CASCADE)
#     cart    = models.ForeignKey(Cart,null=True, blank=True, on_delete=models.CASCADE)
#     viewed = models.BooleanField(default=False)
#     seen   = models.BooleanField(default=False)
#     order_confirmed = models.CharField(max_length=50, default='none')
#     supplier_cancellation = models.BooleanField(default=False)
#     status = models.CharField(max_length=120, default='created')
#     timestamp= models.DateTimeField(auto_now_add=True)

# @receiver(post_save, sender=CartItem)
# def receive_user_orderstatus_msg(sender, instance, created, **kwargs):
#     if instance.order_confirmed == 'confirmed' or instance.order_confirmed == 'rejected' :
#         User_Order_Status_Notification.objects.get_or_create(product = instance.product,
#                                 order_confirmed = instance.order_confirmed,
#                                 status = instance.status,
#                                 cart = instance.cart,
#                             )
#         send_mail('Erenta:Your Order has been'+ instance.order_confirmed , 'Dear User, Your Order has been' + instance.status +'Successfully. Thanks for being here.', 'erentajapan@gmail.com', [instance.cart.user.email,])



class Supplier_Order_Notification(models.Model):
    viewed = models.BooleanField(default=False)
    seen   = models.BooleanField(default=False)
    status = models.CharField(max_length=120, default='created')
    product = models.ForeignKey(Product_description,null=True,blank=True,on_delete=models.CASCADE)
    cart    = models.ForeignKey(Cart,null=True, blank=True, on_delete=models.CASCADE)
    timestamp= models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=CartItem)
def receive_paid_ordersuccess_msg(sender,instance,created, **kwargs):
    if instance.status == 'paid':
        Supplier_Order_Notification.objects.get_or_create(product = instance.product,
                                status = instance.status,
                                cart = instance.cart,
                            )
        send_mail('Erenta:Congratulations you received an Order', 'Dear User, You received an Order of' + instance.product.product_name +' which will be delivered on' + str(instance.start_date) + '. Thanks for being here.', 'erentajapan@gmail.com', [instance.product.user.email,])



class Order_current_status(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    cart   = models.ForeignKey(Cart,null=True,blank=True, on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)
    supplier_viewed = models.BooleanField(default=False)
    seen   = models.BooleanField(default=False)
    supplier_seen = models.BooleanField(default=False)
    order_confirmed = models.CharField(max_length=50, default='none')
    supplier_cancellation = models.BooleanField(default=False)
    product = models.ForeignKey(Product_description,null=True,blank=True,on_delete=models.CASCADE)
    status     = models.CharField(max_length=50, default='paid')
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=CartItem)
def Item_order_status_msg(sender,instance,created, **kwargs):
    if instance.order_confirmed == 'confirmed' or instance.order_confirmed == 'rejected' or instance.status == 'shipped' or instance.status == 'returned back' or instance.status == 'refund requested' or  instance.refund_granted == True  or instance.status == 'cancellation request' or instance.cancel_granted == True:
        Order_current_status.objects.create(user = instance.cart.user,
                                order_confirmed = instance.order_confirmed,
                                status = instance.status,
                                cart = instance.cart,
                                product = instance.product,
                                
        )
    # elif instance.order_confirmed == 'confirmed' or instance.order_confirmed == 'rejected':
    #     Order_current_status.objects.get_or_create(
    #                             user = instance.cart.user.email,
    #                             order_confirmed = instance.order_confirmed,
    #                             status = instance.status,
    #                             cart = instance.cart,
    #                             product = instance.product,
    #                         )
    if instance.order_confirmed == 'none' and instance.status=='paid':
        send_mail('Erenta: Your Order has been'+ instance.status +". Please wait for confirmation from supplier.",'Dear ' + instance.cart.user.full_name+ ', Your Order has been' + instance.status +'Successfully. Thanks for being here.', 'erentajapan@gmail.com', [instance.cart.user.email,])

    elif instance.order_confirmed == 'confirmed' or instance.order_confirmed == 'rejected' and instance.status == 'paid':
        send_mail('Erenta: Your Order has been'+ instance.order_confirmed , 'Dear ' + instance.cart.user.full_name+ ', Your Order has been' + instance.status +'Successfully. Thanks for being here.', 'erentajapan@gmail.com', [instance.cart.user.email,])

    else: 
        if instance.status != 'created':
            send_mail('Erenta: Your Order has been'+ instance.status + "successfully.",'Dear ' + instance.cart.user.full_name+ ', Your Order has been' + instance.status +'Successfully. Thanks for being here.', 'erentajapan@gmail.com', [instance.cart.user.email,])
