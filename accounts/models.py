from datetime import timedelta
import random
import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from django.contrib.auth import get_user_model
from django.utils import timezone
from stdimage.models import StdImageField
from stdimage.validators import MaxSizeValidator
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.core.mail import send_mail
from Ecommerce_Intern.utils import random_string_generator,unique_key_generator
from django.template.loader import get_template
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator

#send_mail(subject, message, from_email, recipient_list, html_message)
DEFAULT_ACTIVATION_DAYS = getattr(settings, 'DEFAULT_ACTIVATION_DAYS', 7)

ACCOUNT_TYPE = (
    (('Overdraft Account'), ('Overdraft Account')),
    (('Saving Account'), ('Saving Account')),
    (('Current Account'), ('Current Account'))
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
        user_obj.is_active = is_active
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

def get_filename_ext(filepath):
    base_name=os.path.basename(filepath)
    name, ext=os.path.splitext(base_name)
    return name,ext


def upload_image_path(instance, filename):
    
    new_filename=random.randint(1,399900000)
    name,ext=get_filename_ext(filename)
    final_filename='{new_filename} {ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
        )
# Create your models here.
# def validate_image(profile_image):
#         file_size = profile_image.file.size
#         limit_mb = 1
#         if file_size > limit_mb * 1024 * 1024:
#             raise ValidationError("Max size of file is %s MB" % limit_mb)

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255,unique=True,null=True)
    full_name = models.CharField(max_length=255,blank=True,null=True)
    profile_image = StdImageField(upload_to=upload_image_path,null=True,blank=True,validators=[MaxSizeValidator(1050, 1050)])
    is_active = models.BooleanField(default=True) # can login
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    update    = models.DateTimeField(auto_now=True)

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
        if self.is_admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin
    
    # @property
    # def is_active(self):
    #     return self.active

class EmailActivationQuerySet(models.query.QuerySet):
    def confirmable(self):
        DEFAULT_ACTIVATION_DAYS
        now = timezone.now()
        start_range = now- timedelta(days=DEFAULT_ACTIVATION_DAYS)
        # does my object have a timestamp in here
        end_range = now
        return self.filter(
            activated = False,
            forced_expired = False
        ).filter(
            timestamp__gt = start_range,
            timestamp__lte = end_range
        )


class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(self.model, using=self._db)
    
    def confirmable(self):
        return self.get_queryset().confirmable()
    
    def email_exists(self, email):
        return self.get_queryset().filter(
            Q(email=email) | 
            Q(user__email=email)
            ).filter(activated=False)

class EmailActivation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    key = models.CharField(max_length=120, blank=True, null=True)
    activated = models.BooleanField(default=False)
    forced_expired = models.BooleanField(default=False)
    expires = models.IntegerField(default=7) # 7 days
    timestamp = models.DateTimeField(auto_now_add=True)
    update    = models.DateTimeField(auto_now=True)

    objects = EmailActivationManager()

    def __str__(self):
        return self.email
    
    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable() # one object
        if qs.exists():
            return True
        return False
    
    def activate(self):
        if self.can_activate():
            # pre activation signal for user
            user = self.user
            user.is_active = True
            user.save()
            # post activation signal for user
            self.activated = True
            self.save()
            return True
        return False

    
    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False

    def send_activation(self):
        if not self.activated and not self.forced_expired:
            if self.key:
                base_url = getattr(settings, 'BASE_URL', 'https://rent-now.herokuapp.com')
                key_path = reverse("account:email-activate",kwargs={"key":self.key}) #use reverse
                path = "{base}{path}".format(base=base_url, path=key_path)
                context = {
                    'path': path,
                    'email': self.email
                }
                
                txt_ = get_template("registration/emails/verify.txt").render(context)
                html_ = get_template("registration/emails/verify.html").render(context)
                subject = '1 Click email verification'
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [self.email]
                sent_mail = send_mail(
                            subject,
                            txt_,
                            from_email,
                            recipient_list,
                            html_message=html_,
                            fail_silently= False,
                            )
                return sent_mail
        return False

def pre_save_email_activation(sender, instance, *args, **kwargs):
    if not instance.activated and not instance.forced_expired:
        if not instance.key:
            instance.key = unique_key_generator(instance)
pre_save.connect(pre_save_email_activation, sender=EmailActivation)


def post_save_user_create_receiver(sender,instance, created, *args, **kwargs):
    if created:
        obj = EmailActivation.objects.create(user=instance, email = instance.email)
        obj.send_activation() 
post_save.connect(post_save_user_create_receiver, sender=User)




class GuestEmail(models.Model):
    email     = models.EmailField()
    active    = models.BooleanField(default=True)
    update    = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email




    
    



class Supplier(models.Model):
    Nick_name = models.CharField(max_length=50, unique=True, null=True, blank=True)
    Shop_name = models.CharField(max_length=100,blank=True,null=True)
    email     = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    Address_Line1 = models.CharField(max_length=555,blank=True,null=True)
    Address_Line2 = models.CharField(max_length=100,blank=True,null=True)
    Postal_code = models.IntegerField(blank=True,null=True)
    City = models.CharField(max_length=55,blank=True,null=True)
    Country = models.CharField(max_length=20, blank=True, null=True)
    Mobile_number = models.CharField(max_length=15,blank=True,null=True)
    receive_message_time = models.CharField(max_length=50, null=True, blank=True)
    #Shop_registration_number=models.CharField(max_length=50,blank=True,null=True)
    #bank_account_number = models.IntegerField(blank=True, null=True)
    is_supplier = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True) # can login
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("email"),)


    def __str__(self):
        return '%s' %(self.email)

class Bank_Account_Detail(models.Model):
    Account_holder_name = models.CharField(max_length=100)
    Account_number = models.CharField(max_length=25)
    IFSC_code = models.CharField(max_length=20)
    Account_type = models.CharField(choices=ACCOUNT_TYPE, max_length=25)
    email = models.OneToOneField(settings.AUTH_USER_MODEL,unique=True, on_delete=models.CASCADE, null=True)
    supplier = models.OneToOneField(Supplier,on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True) # can login
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return '%s %s'%(self.email, self.Account_holder_name)



    





    