from django.db import models
from django.utils import timezone
from datetime import timedelta

MOVEMENT_TYPES = [
    ('RESERVE', 'Reserve'),
    ('RELEASE', 'Release'),
    ('SHIP', 'Ship'),
    ('RESTOCK', 'Restock'),
    ('ADJUSTMENT', 'Adjustment'),
    ('WRITE_OFF', 'Write Off'),
    ('RETURN', 'Return'),
]



def default_ttl():
    return timezone.now() + timedelta(minutes=15)

class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.sku} - {self.name}"


class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.CharField(max_length=100)
    on_hand = models.IntegerField()
    reserved = models.IntegerField()
    low_stock_threshold = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'warehouse')

    @property
    def available(self):
        return self.on_hand - self.reserved

class InventoryMovement(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    order_id = models.CharField(max_length=100, null=True, blank=True)
    reservation_id = models.CharField(max_length=100, null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    idempotency_key = models.CharField(max_length=100, unique=True, null=True, blank=True)
    reserved_at = models.DateTimeField(auto_now_add=True)
    ttl_expires_at = models.DateTimeField(default=default_ttl)
    created_at = models.DateTimeField(auto_now_add=True)


    class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.CharField(max_length=100)
    on_hand = models.IntegerField(default=0)
    reserved = models.IntegerField(default=0)
    threshold = models.IntegerField(default=5)  # 🔔 Alert if below this
    updated_at = models.DateTimeField(auto_now=True)

    def is_low_stock(self):
        return (self.on_hand - self.reserved) < self.threshold

