from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, is_active=True, is_staff=False , is_admin=False):
        if not email:
            raise ValueError("User must have an Email Address")
        if not password:
            raise ValueError("User must have Password")
        if not full_name:
            raise ValueError("full name is required")
        
        user_obj = self.model(
            email = self.normalize_email(email),
            full_name = full_name,
            
        
        )
        user_obj.set_password(password) #set user password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self,email, full_name, password=None):
        user = self.create_user(
            email,
            full_name,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self,email,full_name, password=None):
        user = self.create_user(
            email,
            full_name,
            password=password,
            is_staff= True,
            is_admin=True
        )
        return user

# Create your models here.
class User(AbstractBaseUser):
    email = models.EmailField(max_length=255,unique=True,null=True)
    full_name = models.CharField(max_length=255,blank=True,null=True)
    is_active = models.BooleanField(default=True) # can login
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    #confirm = models.BooleanField(default = True)  # confirmed email or not
    #confirmed_date = models.DateTimeField(default=True) 


    USERNAME_FIELD = 'email' #username
    # username and password are required by default
    REQUIRED_FIELDS = ['full_name'] # ['full_name'] 
    objects = UserManager()

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.full_name
    
    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin
    
    # @property
    # def is_active(self):
    #     return self.active


class GuestEmail(models.Model):
    email     = models.EmailField()
    active    = models.BooleanField(default=True)
    update    = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email




    
    



class Supplier(models.Model):
    # email = models.EmailField(max_length=255,unique=True)
    # full_name = models.CharField(max_length=255,blank=True,null=True)
    # password1 = models.CharField(max_length=16,null=True)
    # password2 = models.CharField(max_length=16,null=True)
    
    Shop_name = models.CharField(max_length=100,blank=True,unique=True,null=True)
    Address_Line1 = models.CharField(max_length=555,blank=True,null=True)
    Address_Line2 = models.CharField(max_length=100,blank=True,null=True)
    Postal_code = models.IntegerField(blank=True,null=True)
    City = models.CharField(max_length=55,blank=True,null=True)
    Mobile_number = models.IntegerField(blank=True,null=True)
    Shop_registration_number=models.CharField(max_length=50,blank=True,null=True)
    is_active = models.BooleanField(default=True) # can login
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.Shop_name)
    





    