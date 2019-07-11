from django.db import models
import math
from carts.models import Cart
from django.urls import reverse
from django.conf import settings
from billing.models import BillingProfile
from products.models import Product_description
from addresses.models import Address
from django.db.models.signals import pre_save , post_save
from Ecommerce_Intern.utils import unique_order_id_generator
from accounts.models import User
User = settings.AUTH_USER_MODEL

# Create your models here.
ORDER_STATUS_CHOICES = (
    ('created','Created'),
    ('paid', 'Paid'),
    ('shipped','Shipped'),
    ('refunded','Refunded'),
)

class OrderManagerQuerySet(models.query.QuerySet):
    def by_request(self,request):
        billing_profile,created=BillingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)
    
    
    def not_created(self):
        return self.exclude(status='created')

class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderManagerQuerySet(self.model,using=self._db)

    def by_request(self,request):
        return self.get_queryset().by_request(request)
    
    # def get_by_id(self):
    #     qs = Order.objects.cart.products.filter(registered_email=registered_email)
    #     # if qs.count()==1:
    #     #     return qs.first
    #     # else:
    #     #     return None
    #     return qs

    def new_or_get(self,billing_profile,cart_obj):
        created = False
        qs=self.get_queryset().filter(billing_profile=billing_profile, cart=cart_obj, active=True, status='created')
        if qs.count()==1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(billing_profile=billing_profile , cart=cart_obj)
            created = True
        return obj, created 
    

class Order(models.Model):
    billing_profile    = models.ForeignKey(BillingProfile, null=True,blank=True, on_delete=models.CASCADE)
    order_id           = models.CharField( max_length=120, blank=True)
    shipping_address   = models.ForeignKey(Address, related_name="shipping_address", null=True,blank=True, on_delete=models.CASCADE)
    billing_address    = models.ForeignKey(Address, related_name="billing_address", null=True,blank=True, on_delete=models.CASCADE)
    cart               = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status             = models.CharField(max_length=120, default='created')
    shipping_total     = models.DecimalField(default=15,max_digits=50,decimal_places=2)
    total              = models.DecimalField(default=0.00,max_digits=50,decimal_places=2)
    active             = models.BooleanField(default=True)
    being_delivered    = models.BooleanField(default=False)
    received           = models.BooleanField(default=False)
    refund_requested   = models.BooleanField(default=False)
    refund_granted     = models.BooleanField(default=False)
    updated            = models.DateTimeField(auto_now=True)
    timestamp          = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_id


    objects = OrderManager()
    class Meta:
        ordering = ['-timestamp','-updated']
        
    def get_absolute_url(self):
        return reverse("orders:detail", kwargs={'order_id':self.order_id})
    
    def get_absolute_url1(self):
        return reverse("orders:supplierorderdetail", kwargs={'order_id':self.order_id})

    def get_status(self):
        if self.status == "refunded":
            return "Refunded order"
        elif self.status == "shipped":
            return "Shipped"
        return "Shipping soon :)"
        

    def update_total(self):
        cart_total=self.cart.total
        shipping_total=self.shipping_total
        
        new_total = math.fsum([cart_total, shipping_total])
        formatted_total = format(new_total, '.2f')
        self.total=formatted_total
        self.save()
        return new_total
     
    def check_done(self):
        billing_profile = self.billing_profile
        shipping_address = self.shipping_address
        billing_address = self.billing_address
        total = self.total
        if billing_profile and billing_address and shipping_address and total>0:
            return True
        return False
     
    def mark_paid(self):
        if self.check_done():
            self.status = "paid"
            self.save()
        return self.status


def pre_save_create_order_id(sender,instance,*args,**kwargs):
    if not instance.order_id:
        instance.order_id=unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)
pre_save.connect(pre_save_create_order_id, sender=Order)

def post_save_cart_total(sender,created,instance,*args,**kwargs):
    if not created:
        cart_obj =instance
        cart_total=cart_obj.total
        cart_id = cart_obj.id
        qs= Order.objects.filter(cart__id=cart_id)
        if qs.count()==1:
            order_obj=qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)

def post_save_order(sender,instance,created,*args,**kwargs):
    if created:
        instance.update_total()

post_save.connect(post_save_order, sender=Order)




class Refund(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email    = models.EmailField()

    def __str__(self):
        return f"{self.pk}"
