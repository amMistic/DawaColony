from django.urls import reverse
from django.db import models
from django.utils.text import slugify
from accounts.models import User


# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('PRESCRIPTION_MEDICINES', 'Prescription Medicines'),
        ('HEALTHCARE_DEVICES', 'Healthcare Devices'),
        ('SURGICAL_PRODUCTS', 'Surgical Products'),
        ('AYURVEDIC_MEDICINES', 'Ayurvedic Medicines'),
        ('PERSONAL_CARE', 'Personal Care'),
        ('BEAUTY_PRODUCTS', 'Beauty Products'),
        ('GROCERY_PRODUCTS', 'Grocery Products'),
        ('FITNESS_ENTHUSIASTS', 'Fitness Enthusiasts'),
        ('BABY_PRODUCTS', 'Baby Products'),
        ('SEX_AWARE_PRODUCTS', 'Sex Aware Products'),
        ('HOUSEHOLD_PRODUCTS', 'Household Products'),
        ('PET_PRODUCTS', 'Pet Products'),
    ]
    
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=64, choices=CATEGORY_CHOICES, )
    description = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=10000, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to=f'products/create/', blank=True, null=True)
    mrp = models.DecimalField(max_digits=10000, decimal_places=2, help_text="Maximum Retail Price")
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    specifications = models.JSONField(default=dict, blank=True)
    manufacturer = models.CharField(max_length=200, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    prescription_required = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('products:product-detail', kwargs={'slug': self.slug})
    
    def calculate_discount(self):
        if self.mrp > self.price:
            return ((self.mrp - self.price) / self.mrp) * 100
        return 0
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Product.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            
            self.slug = slug
        self.discount_percentage = self.calculate_discount()
        super().save(*args, **kwargs)
        
    class Meta:
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['price']),
            models.Index(fields=['created_at']),
        ]