from django.db import models
from accounts.models import User
from products.models import Product

# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING','Pending'),
        ('PROCESSING','Processing'),
        ('SHIPPED','Shipped'),
        ('DELIVERED','Delivered'),
        ('CANCELLED','Cancelled')
    ]
    
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_orders')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits = 10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f" Order #{self.id} - {self.product.name}"