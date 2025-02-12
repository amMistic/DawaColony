from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Create your models here.
class User(AbstractUser):
    ADMIN = 'Admin'
    SELLER = 'Seller'
    CUSTOMER = 'Customer'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (SELLER, 'Seller'),
        (CUSTOMER, 'Customer'),
    ]
    
    MALE = 'male'
    FEMALE = 'female'
    OTHERS = 'others'
    
    GENDER_CHOICES = [
            (MALE, 'Male'),
            (FEMALE, 'Female'),
            (OTHERS, 'Others'),    
    ]
    
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES, default=MALE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=CUSTOMER)
    shopname = models.CharField(max_length=64, default=' ')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(max_length=256, blank=True)
    shop_invoice = models.ImageField(upload_to='become-seller/',default=None, null=True, blank=True)
    
    
    def clean(self):
        if self.role == self.SELLER:
            if self.shopname == ' ':
                raise ValidationError({'shopname' : 'Shop name is required.'})
            if not  self.shop_invoice:
                raise ValidationError({'shop_invoice' : 'Shop incvoice ensure your authenticity, you have to upload the invoice.'})
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
            
                    
    def is_admin_user(self):
        return self.role == self.ADMIN
    
    def is_seller_user(self):
        return self.role == self.SELLER
    
    def is_customer_user(self):
        return self.role == self.CUSTOMER

