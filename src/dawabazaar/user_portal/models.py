from django.db import models
from accounts.models import User


# Create your models here.
class Address(models.Model):

    ADDRESS_TYPE_CHOICES = [
        ("HOME", "Home"),
        ("WORK", "Work"),
        ("OTHER", "other"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    full_name = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=15)
    alternative_phone_number = models.CharField(max_length=15, null=True, blank=True)
    pincode = models.CharField(max_length=6)
    address_line_1 = models.CharField(max_length=128, default='No address')
    address_line_2 = models.CharField(max_length=128, blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=125)
    state = models.CharField(max_length=125)
    address_type = models.CharField(max_length=255, choices=ADDRESS_TYPE_CHOICES)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_default", "-created_at"]
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.full_name}'s {self.address_type} Address"
    
    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user).exclude(id=self.id).update(is_default=False)
        super().save(*args, **kwargs)
