from django.db import models
from django.conf import settings
from products.models import Product_description

User = settings.AUTH_USER_MODEL
SIZES = (
    (('Not appicable'),('Not applicable')),
    (('S'), ('S')),
    (('M'), ('M')),
    (('L'), ('L')),
    (('XL'),('XL')),

)


# Create your models here.
class OtherDetails(models.Model):
    user    = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    product = models.ForeignKey(Product_description,null=True,blank=True,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size    = models.CharField(choices=SIZES,default=1,max_length=20)
    days    = models.IntegerField(default=1)
    other_details = models.TextField(blank=True,null=True,max_length=200)

    def __str__(self):
        return str(self.user)  
