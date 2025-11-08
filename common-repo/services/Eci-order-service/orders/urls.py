# orders/urls.py
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet  # you must have this viewset

router = DefaultRouter()
router.register(r"orders", OrderViewSet, basename="order")

urlpatterns = router.urls
