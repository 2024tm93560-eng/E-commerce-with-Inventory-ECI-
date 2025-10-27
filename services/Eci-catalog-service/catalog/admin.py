# Register your models here.
# catalog/admin.py
from django.contrib import admin
from .models import Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku","name","category","price","is_active","updated_at")
    search_fields = ("sku","name","category")
    list_filter = ("is_active","category")
