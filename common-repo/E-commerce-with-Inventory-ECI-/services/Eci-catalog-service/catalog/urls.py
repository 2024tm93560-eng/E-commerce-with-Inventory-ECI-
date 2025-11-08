# catalog/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, health

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')  # <-- NO leading slash

urlpatterns = [
    path('health/', health, name='catalog-health'),
    path('', include(router.urls)),  # yields /v1/catalog/products/...
]
