from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Product, Inventory, InventoryMovement
from .serializers import ProductSerializer, InventorySerializer, InventoryMovementSerializer
import csv
import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from inventory.models import Inventory, Product
from django.db import transaction

from rest_framework.decorators import api_view
from rest_framework.response import Response
from inventory.models import Inventory, Product
from django.db import transaction

from rest_framework.decorators import api_view
from rest_framework.response import Response
from inventory.models import Inventory, Product, InventoryMovement
from django.db import transaction

@api_view(['POST'])
def reserve_inventory(request):
    try:
        product_id = int(request.data.get('product_id'))
        quantity = int(request.data.get('quantity'))
        warehouse = request.data.get('warehouse')
        idempotency_key = request.data.get('idempotency_key')
    except (TypeError, ValueError):
        return Response({'error': 'Invalid input'}, status=400)

    if not all([product_id, quantity, warehouse, idempotency_key]):
        return Response({'error': 'Missing required fields'}, status=400)

    try:
        product = Product.objects.get(id=product_id)
        inventory = Inventory.objects.get(product=product, warehouse=warehouse)
    except (Product.DoesNotExist, Inventory.DoesNotExist):
        return Response({'error': 'Product or inventory not found'}, status=404)

    if InventoryMovement.objects.filter(idempotency_key=idempotency_key).exists():
        return Response({'status': 'already processed'}, status=200)

    available = inventory.on_hand - inventory.reserved
    if available < quantity:
        return Response({'error': 'Insufficient stock', 'available': available}, status=400)

    with transaction.atomic():
        inventory.reserved += quantity
        inventory.save()

        InventoryMovement.objects.create(
            product=product,
            warehouse=warehouse,
            quantity=quantity,
            movement_type='RESERVE',
            idempotency_key=idempotency_key
        )

       if inventory.is_low_stock():
       logger.warning(f"Low stock alert: Product {product.id} in {warehouse} has only {inventory.on_hand - inventory.reserved} available.")

    return Response({'status': 'reserved'}, status=201)


@api_view(['POST'])
def release_inventory(request):
    product_id = request.data.get('product_id')
    quantity = int(request.data.get('quantity'))
    warehouse = request.data.get('warehouse')
    idempotency_key = request.data.get('idempotency_key')

    try:
        product = Product.objects.get(id=product_id)
        inventory = Inventory.objects.get(product=product, warehouse=warehouse)
    except (Product.DoesNotExist, Inventory.DoesNotExist):
        return Response({'error': 'Product or inventory not found'}, status=404)

    if InventoryMovement.objects.filter(idempotency_key=idempotency_key).exists():
        return Response({'status': 'already processed'}, status=200)

    with transaction.atomic():
        inventory.reserved = max(0, inventory.reserved - quantity)
        inventory.save()

        InventoryMovement.objects.create(
            product=product,
            warehouse=warehouse,
            quantity=quantity,
            movement_type='RELEASE',
            idempotency_key=idempotency_key
        )

    return Response({'status': 'released'}, status=201)

@api_view(['POST'])
def ship_inventory(request):
    product_id = request.data.get('product_id')
    quantity = int(request.data.get('quantity'))
    warehouse = request.data.get('warehouse')
    idempotency_key = request.data.get('idempotency_key')

    try:
        product = Product.objects.get(id=product_id)
        inventory = Inventory.objects.get(product=product, warehouse=warehouse)
    except (Product.DoesNotExist, Inventory.DoesNotExist):
        return Response({'error': 'Product or inventory not found'}, status=404)

    if InventoryMovement.objects.filter(idempotency_key=idempotency_key).exists():
        return Response({'status': 'already processed'}, status=200)

    if inventory.reserved < quantity:
        return Response({'error': 'Not enough reserved stock'}, status=400)

    with transaction.atomic():
        inventory.reserved -= quantity
        inventory.on_hand -= quantity
        inventory.save()

        InventoryMovement.objects.create(
            product=product,
            warehouse=warehouse,
            quantity=quantity,
            movement_type='SHIP',
            idempotency_key=idempotency_key
        )
        if inventory.is_low_stock():
        logger.warning(f"Low stock alert: Product {product.id} in {warehouse} has only {inventory.on_hand - inventory.reserved} available.")

    return Response({'status': 'shipped'}, status=201)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from inventory.models import Product, Inventory, InventoryMovement
from django.db import transaction

@api_view(['POST'])
def restock_inventory(request):
    try:
        product_id = int(request.data.get('product_id'))
        warehouse = request.data.get('warehouse')
        quantity = int(request.data.get('quantity'))
        idempotency_key = request.data.get('idempotency_key')
    except (TypeError, ValueError):
        return Response({'error': 'Invalid input'}, status=400)

    if not all([product_id, warehouse, quantity, idempotency_key]):
        return Response({'error': 'Missing required fields'}, status=400)

    if InventoryMovement.objects.filter(idempotency_key=idempotency_key).exists():
        return Response({'status': 'already processed'}, status=200)

    try:
        product = Product.objects.get(id=product_id)
        inventory = Inventory.objects.get(product=product, warehouse=warehouse)
    except (Product.DoesNotExist, Inventory.DoesNotExist):
        return Response({'error': 'Product or inventory not found'}, status=404)

    with transaction.atomic():
        inventory.on_hand += quantity
        inventory.save()

        InventoryMovement.objects.create(
            product=product,
            warehouse=warehouse,
            quantity=quantity,
            movement_type='RESTOCK',
            idempotency_key=idempotency_key
        )
        if inventory.is_low_stock():
        logger.warning(f"Low stock alert: Product {product.id} in {warehouse} has only {inventory.on_hand - inventory.reserved} available.")

    return Response({'status': 'restocked'}, status=201)

@api_view(['POST'])
def cancel_order_inventory(request):
    order_id = request.data.get('order_id')
    status = request.data.get('status')  # e.g., "CONFIRMED", "UNCONFIRMED"
    items = request.data.get('items')  # list of {product_id, warehouse, quantity}
    idempotency_key = request.data.get('idempotency_key')

    if not all([order_id, status, items, idempotency_key]):
        return Response({'error': 'Missing required fields'}, status=400)

    if InventoryMovement.objects.filter(idempotency_key=idempotency_key).exists():
        return Response({'status': 'already processed'}, status=200)

    with transaction.atomic():
        for item in items:
            try:
                product_id = int(item['product_id'])
                warehouse = item['warehouse']
                quantity = int(item['quantity'])

                product = Product.objects.get(id=product_id)
                inventory = Inventory.objects.get(product=product, warehouse=warehouse)

                inventory.reserved = max(0, inventory.reserved - quantity)
                inventory.save()

                InventoryMovement.objects.create(
                    product=product,
                    warehouse=warehouse,
                    quantity=quantity,
                    movement_type='RELEASE',
                    idempotency_key=idempotency_key + f"-{product_id}-{warehouse}"
                )
            except Exception:
                continue  # skip faulty items

    return Response({'status': 'reservations released'}, status=200)

@api_view(['POST'])
def confirm_delivery(request):
    order_id = request.data.get('order_id')
    items = request.data.get('items')  # list of {product_id, warehouse, quantity}

    if not all([order_id, items]):
        return Response({'error': 'Missing required fields'}, status=400)

    delivered = True

    for item in items:
        try:
            product_id = int(item['product_id'])
            warehouse = item['warehouse']
            quantity = int(item['quantity'])

            product = Product.objects.get(id=product_id)
            inventory = Inventory.objects.get(product=product, warehouse=warehouse)

            if inventory.reserved >= quantity:
                delivered = False
        except Exception:
            delivered = False

    return Response({'order_id': order_id, 'delivered': delivered}, status=200)


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.select_related('product').all()
    serializer_class = InventorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class InventoryMovementViewSet(viewsets.ModelViewSet):
    queryset = InventoryMovement.objects.all()
    serializer_class = InventoryMovementSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        key = data.get('idempotency_key')
        if InventoryMovement.objects.filter(idempotency_key=key).exists():
            return Response({'status': 'already processed'}, status=200)

        try:
            product = Product.objects.get(id=data['product'])
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            inventory = Inventory.objects.get(product=product, warehouse=data['warehouse'])
        except Inventory.DoesNotExist:
            return Response({'error': 'Inventory not found for this product and warehouse'}, status=status.HTTP_404_NOT_FOUND)

        qty = int(data['quantity'])
        movement_type = data['movement_type']

        if movement_type == 'RESERVE':
            if inventory.on_hand - inventory.reserved >= qty:
                inventory.reserved += qty
            else:
                return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)

        elif movement_type == 'RELEASE':
            inventory.reserved = max(0, inventory.reserved - qty)

        elif movement_type == 'SHIP':
            if inventory.reserved >= qty:
                inventory.on_hand -= qty
                inventory.reserved -= qty
            else:
                return Response({'error': 'Not enough reserved stock'}, status=status.HTTP_400_BAD_REQUEST)

        inventory.updated_at = timezone.now()
        inventory.save()

        movement = InventoryMovement.objects.create(
            product=product,
            warehouse=data['warehouse'],
            quantity=qty,
            movement_type=movement_type,
            idempotency_key=data.get('idempotency_key', f"auto-{timezone.now().timestamp()}")
        )
        return Response(InventoryMovementSerializer(movement).data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def low_stock_check(request):
    product_id = request.data.get('product_id')
    warehouse = request.data.get('warehouse')

    try:
        product = Product.objects.get(id=product_id)
        inventory = Inventory.objects.get(product=product, warehouse=warehouse)
    except (Product.DoesNotExist, Inventory.DoesNotExist):
        return Response({'error': 'Product or inventory not found'}, status=404)

    available = inventory.on_hand - inventory.reserved
    return Response({
        'product_id': product_id,
        'warehouse': warehouse,
        'available': available,
        'threshold': inventory.threshold,
        'low_stock': inventory.is_low_stock()
    }, status=200)



