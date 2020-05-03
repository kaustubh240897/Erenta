from django.db import models
import math
import datetime
from django.utils import timezone
from carts.models import Cart,Coupon,Quantity,CartItem
from django.urls import reverse
from django.conf import settings
from billing.models import BillingProfile
from products.models import Product_description
from addresses.models import Address
from django.db.models.signals import pre_save , post_save
from django.dispatch import receiver
from django.db.models import Sum,Avg,Count
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
    def recent(self):
        return self.order_by("-updated","-timestamp")
    
    def get_sales_breakdown(self):
        recent = self.recent().not_refunded().not_created()
        recent_data = recent.totals_data()
        recent_cart_data = recent.carts_data()
                                                                  
        shipped= recent.not_refunded().not_created().by_status(status="shipped")
        shipped_data = shipped.totals_data()
        paid = recent.not_refunded().not_created().by_status(status="paid")
        paid_data = paid.totals_data()
        data = {
            'recent' : recent,
            'recent_data': recent_data,
            'recent_cart_data': recent_cart_data,
            'shipped': shipped,
            'shipped_data': shipped_data,
            'paid': paid,
            'paid_data': paid_data
        }
        return data

    def get_sales_breakdown_supplier(self):
        recent = self.recent().not_refunded().not_created()
        recent_data = recent.totals_data()
        recent_cart_data = recent.supplier_linetotal_data()
                                                                  
        shipped= recent.not_refunded().not_created().by_status(status="shipped")
        shipped_cart_data = shipped.supplier_linetotal_data()
        paid = recent.not_refunded().not_created().by_status(status="paid")
        paid_cart_data = paid.supplier_linetotal_data()
        
        data = {
            'recent' : recent,
            'recent_data': recent_data,
            'recent_cart_data': recent_cart_data,
            'shipped': shipped,
            'shipped_cart_data': shipped_cart_data,
            'paid': paid,
            'paid_cart_data': paid_cart_data
        }
        return data

    def by_weeks_range(self, weeks_ago=1, number_of_weeks=1):
        if number_of_weeks > weeks_ago:
            number_of_weeks = weeks_ago
        days_ago_start = weeks_ago * 7
        days_ago_end = days_ago_start - (number_of_weeks * 7)
        start_date = timezone.now() - datetime.timedelta(days=days_ago_start)
        end_date = timezone.now() - datetime.timedelta(days=days_ago_end)
        return self.by_range(start_date,end_date=end_date)
    
    def by_range(self, start_date, end_date=None):
        if end_date is None:
            return self.filter(updated__gte=start_date)
        return self.filter(updated__gte=start_date).filter(updated__lte=end_date)


    def by_date(self):
        now = timezone.now()
        return self.filter(updated__day=now.day)
    
    def totals_data(self):
        return self.aggregate(Sum("total"), Avg("total"))
    
    
    # def supplier_data(self,request):
    #     return self.filter(cart__cartitem__product__user=self.request.user)
    
    def carts_data(self):
        return self.aggregate(Sum("cart__cartitem__product__cost_per_day"),
                              Avg("cart__cartitem__product__cost_per_day"),
                              Count("cart__cartitem__product")
                              )
    def supplier_linetotal_data(self):
        return self.aggregate(Sum("cart__cartitem__line_total"),
                              Avg("cart__cartitem__line_total"),
                              Count("cart__cartitem__line_total")
                              )
    
    def by_status(self, status='shipped'):
        return self.filter(status=status)
    
    def not_refunded(self):
        return self.exclude(status='refunded')
    
    def not_product_refunded(self):
        return self.exclude(cart__cartitem__refund_requested='True')

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

    def get_absolute_url2(self):
        return reverse("orders:createddetail", kwargs={'order_id':self.order_id})

    def get_status(self):
        if self.status == "refunded":
            return "Refunded order"
        elif self.status == "shipped":
            return "Shipped"
        elif self.status == 'created':
            return 'Unpaid'
        return "Ship soon :)"
        

    def update_total(self):
        cart_total=self.cart.total
        shipping_total=self.shipping_total
        
        new_total = math.fsum([float(cart_total), shipping_total])
        #new_total = new_total- self.coupon.amount
        formatted_total = format(new_total, '.2f')
        self.total=formatted_total
        self.save()
        return new_total
    
    def update_coupon(self):
        coupon_total=self.cart.coupon.amount
        total = self.total
        new_coupon_total = total-coupon_total
        formatted_total = format(new_coupon_total, '.2f')
        self.total = formatted_total
        self.save()
        return new_coupon_total
     
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

def post_save_coupon_total(sender,created,instance,*args,**kwargs):
    if instance.coupon:
        cart_obj =instance
        cart_total=cart_obj.total
        cart_id = cart_obj.id
        qs= Order.objects.filter(cart__id=cart_id)
        if qs.count()==1:
            order_obj=qs.first()
            order_obj.update_coupon()


post_save.connect(post_save_coupon_total, sender=Cart)

def post_save_order(sender,instance,created,*args,**kwargs):
    if created:
        instance.update_total()

post_save.connect(post_save_order, sender=Order)



def post_save_cartitem_status(sender,instance,*args,**kwargs):
    if instance.status == 'paid':
        CartItem.objects.filter(cart=instance.cart).update(status='paid')
post_save.connect(post_save_cartitem_status, sender=Order)


class Refund(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    email = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    timestamp= models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "%s requested refund on %s" %(self.pk, self.timestamp)




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




def post_save_order_quantity_receiver(sender,instance,*args,**kwargs):
    if instance.status == 'paid':
        cart1 = instance.cart
        cart_items = CartItem.objects.filter(cart=cart1)

        for qtyy in cart_items:
            id_list = []
            for x in qtyy.variations.all():
                i = x.id
                id_list.append(i)
                print("cart product variation id",id_list)
            id_list1=[]
            q= Quantity.objects.filter(product__cartitem__cart=instance.cart)
            if q.count()>0:
                for z in q:
                    x = z.variations.all()
                    break

                if x.count()==0:
                    for c in q:
                        qs = Quantity.objects.filter(id=c.id).first()
                        print("qqqqqqqqqqqqqqqqqqqc",qtyy.quantity)
                        qs.quantity = qs.quantity-int(qtyy.quantity)
                        qs.save()
                        break
                        
                        
                else:
                    for y in q:
                        id_list1=[]
                        j=y.variations.all()
                        j1 = y.id
                        print("quantity model ki id",j1)
                        for z in j:
                            k=z.id
                            id_list1.append(k)
                            print("quantity model ke variation ki id",id_list1)
                            if(id_list==id_list1):
                                j2 = j1
                                q1 = Quantity.objects.get(id=j2)
                                print("qqqqqqqqqqqqqqqqqqqq",q1.quantity)
                                print("qqqqqqqqqqqqqqqqqqqc",qtyy.quantity)
                                q1.quantity = q1.quantity+(1/2)-int(qtyy.quantity)
                                q1.save()
                                break
    
    
    
post_save.connect(post_save_order_quantity_receiver , sender=Order)