from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

class Product(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    sku        = models.CharField(max_length=64, unique=True, db_index=True)
    name       = models.CharField(max_length=255)
    category   = models.CharField(max_length=120, db_index=True)
    price      = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sku}-{self.name}"
    
