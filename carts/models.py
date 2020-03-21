from django.conf import settings
from django.db import models
from decimal import Decimal
from django.db.models.signals import pre_save , post_save, m2m_changed
from products.models import Product_description,Variation
from otherdetails.models import OtherDetails
from datetime import date
from django.dispatch import receiver
from django.db.utils import IntegrityError
User = settings.AUTH_USER_MODEL




class CartManager(models.Manager):
    def new_or_get(self , request):
        cart_id = request.session.get("cart_id", None)
        qs=self.get_queryset().filter(id=cart_id)
        if qs.count() ==1:
            new_obj = False
            cart_obj=qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj= Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
            cart_id = cart_obj.id
        return cart_obj, new_obj
    
    
    def new(self,user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj=user
            
        return self.model.objects.create(user=user_obj)


class CartItem(models.Model):
    cart = models.ForeignKey('Cart', null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product_description,null=True,blank=True,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    start_date = models.DateField(null=True,blank=True,auto_now=False, auto_now_add=False)
    end_date = models.DateField(null=True,blank=True,auto_now=False, auto_now_add=False)
    days  =   models.IntegerField(default = 1, null=True, blank=True)
    variations = models.ManyToManyField(Variation,blank=True)
    line_total = models.DecimalField(default=0.00,max_digits=1000,decimal_places=2)
    refund_requested   = models.BooleanField(default=False)
    refund_granted     = models.BooleanField(default=False) 
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        try:
            return str(self.cart.id)
        except:
            return self.product.product_name
    
    def get_amount_saved(self):
        return self.quantity * (self.product.cost_per_day-self.product.discount_price) * (self.days)

def pre_save_cartitem_receiver(sender, instance,*args,**kwargs):
    if instance.product.discount_price:
        instance.line_total= Decimal(instance.quantity)*(instance.product.discount_price) * Decimal(instance.days)
    else:
        instance.line_total= Decimal(instance.quantity)*(instance.product.cost_per_day) * Decimal(instance.days)

pre_save.connect(pre_save_cartitem_receiver , sender=CartItem)



class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    #items = models.ManyToManyField(CartItem, null=True, blank=True)
    #products = models.ManyToManyField(Product_description,blank=True)
    #other = models.ManyToManyField(OtherDetails,blank=True)
    subtotal = models.DecimalField(default=0, max_digits=50, decimal_places=2 )
    total = models.DecimalField(default=0.00, max_digits=50, decimal_places=2 )
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)
    



# def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
#     if action =='post_add' or action =='post_remove' or action =='post_clear':
#         items = instance.items.all()
#         total=0
#         for x in items:
#             line_total = float(x.product.cost_per_day)*(x.quantity)
#             total += line_total
#         if instance.subtotal != total:
#             instance.subtotal=total
#             instance.save()
# m2m_changed.connect(m2m_changed_cart_receiver, sender = Cart.items.through)
    
def pre_save_cart_receiver(sender, instance,*args,**kwargs):
    if instance.subtotal > 0:
        instance.total=format((Decimal(instance.subtotal) * Decimal(1.1)),'.2f')
    else:
        instance.total=0.00
pre_save.connect(pre_save_cart_receiver , sender=Cart)


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.DecimalField(default=0.00, max_digits=50, decimal_places=2 )

    def __str__(self):
        return self.code






class Quantity(models.Model):
    product = models.ForeignKey(Product_description,on_delete=models.CASCADE)
    # color = models.CharField(max_length=100,default=None)
    # size = models.CharField(max_length=100,default=None)
    variations = models.ManyToManyField(Variation,blank=True) 
    quantity = models.IntegerField(default=1)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)

    def __str__(self):
        return str(self.product.slug)
        # return u", ".join([a.title for a in self.variations.all()])


# @receiver(m2m_changed, sender=Quantity.variations.through)
# def verify_uniqueness(sender, **kwargs):
#     action = kwargs.get('action', None)
#     variations = kwargs.get('pk_set', None)

#     if action == 'pre_add':
#         count = 0
#         for v in variations:
#             if Quantity.objects.filter(variations=v):
#                 count = count +1
#                 if count==2:
#                     raise IntegrityError('Quantity of this already exists for variation')


# def post_save_cartitem_receiver(sender,instance,*args,**kwargs):
#     if instance.cart:
#         variation1 = instance.variations.all()
#         id_list = []
#         for x in variation1:
#             i = x.id
#             id_list.append(i)
#             print("cart product variation id",id_list)
#         id_list1=[]
#         q= Quantity.objects.filter(product__id=instance.product.id)
#         if q.count()>0:
#             for z in q:
#                 x = z.variations.all()
#                 break

#             if x.count()==0:
#                 for c in q:
#                     qs = Quantity.objects.filter(id=c.id).first()
#                     print("qqqqqqqqqqqqqqqqqqqc",instance.quantity)
#                     qs.quantity = qs.quantity-int(instance.quantity)
#                     qs.save()
#                     break
                    
#             else:
#                 for y in q:
#                     id_list1=[]
#                     j=y.variations.all()
#                     j1 = y.id
#                     print("quantity model ki id",j1)
#                     for z in j:
#                         k=z.id
#                         id_list1.append(k)
#                         print("quantity model ke variation ki id",id_list1)
#                         if(id_list==id_list1):
#                             j2 = j1
#                             q1 = Quantity.objects.get(id=j2)
#                             print("qqqqqqqqqqqqqqqqqqqq",q1.quantity)
#                             print("qqqqqqqqqqqqqqqqqqqc",instance.quantity)
#                             q1.quantity = q1.quantity+(1/2)-int(instance.quantity)
#                             q1.save()
#                             break
#     else:
#         variation1 = instance.variations.all()
#         id_list = []
#         for x in variation1:
#             i = x.id
#             id_list.append(i)
#             print("cart product variation id",id_list)
#         id_list1=[]
#         q= Quantity.objects.filter(product__id=instance.product.id)
#         if q.count() ==1:
#             for c in q:
#                 q1 = Quantity.objects.get(id=c.id)
#                 q1.quantity = q1.quantity+int(instance.quantity)
#                 q1.save()
#                 break
#         else:
#             for y in q:
#                 id_list1=[]
#                 j=y.variations.all()
#                 j1 = y.id
#                 print("quantity model ki id",j1)
#                 for z in j:
#                     k=z.id
#                     id_list1.append(k)
#                     print("quantity model ke variation ki id",id_list1)
#                     if(id_list==id_list1):
#                         j2 = j1
#                         q1 = Quantity.objects.get(id=j2)
#                         q1.quantity = q1.quantity+int(instance.quantity)
#                         q1.save()
#                         break
    
    
# post_save.connect(post_save_cartitem_receiver , sender=CartItem)