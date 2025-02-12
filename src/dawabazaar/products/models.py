from django.db import models
from django.utils.text import slugify
from accounts.models import User


# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('MEDICINE', 'medicine'),
        ('HEALTHCARE', 'Healthcare'),
        ('WELLNESS', 'Wellness'),
        ('PERSONAL_CARE', 'Personal Care'),
    ]
    
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=64, choices=CATEGORY_CHOICES, )
    description = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=10000, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='product/create/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        