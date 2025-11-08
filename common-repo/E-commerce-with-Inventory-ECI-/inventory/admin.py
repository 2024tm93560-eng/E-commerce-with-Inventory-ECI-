
from django.contrib import admin
from .models import Product, Inventory, InventoryMovement

admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(InventoryMovement)

