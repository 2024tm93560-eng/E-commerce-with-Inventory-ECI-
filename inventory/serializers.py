from rest_framework import serializers
from .models import Product, Inventory, InventoryMovement

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    sku = serializers.CharField(source='product.sku', read_only=True)
    name = serializers.CharField(source='product.name', read_only=True)
    category = serializers.CharField(source='product.category', read_only=True)
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Inventory
        fields = [
            'id', 'product', 'sku', 'name', 'category', 'price',
            'warehouse', 'on_hand', 'reserved', 'available',
            'threshold', 'updated_at'
        ]

class InventoryMovementSerializer(serializers.ModelSerializer):
    sku = serializers.CharField(source='product.sku', read_only=True)

    class Meta:
        model = InventoryMovement
        fields = '__all__'
