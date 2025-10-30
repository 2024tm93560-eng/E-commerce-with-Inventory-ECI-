from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet,
    InventoryViewSet,
    InventoryMovementViewSet,
    reserve_inventory,
    release_inventory, 
    ship_inventory,
    restock_inventory,
    cancel_order_inventory,
    confirm_delivery,
    low_stock_check,

)


router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'inventory', InventoryViewSet)
router.register(r'movements', InventoryMovementViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('v1/inventory/reserve/', reserve_inventory,),
    path('v1/inventory/release/', release_inventory),
    path('v1/inventory/ship/', ship_inventory),
    path('v1/inventory/restock/', restock_inventory),
    path('v1/inventory/cancel-order/', cancel_order_inventory),
    path('v1/inventory/confirm-delivery/', confirm_delivery),
    path('v1/inventory/low-stock-check/', low_stock_check),

]
