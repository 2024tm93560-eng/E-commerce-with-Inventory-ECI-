# order_service/urls.py
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static  # <-- needed

def root(_):
    return JsonResponse({"service": "orders", "status": "ok"})

def healthz(_):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path("", root),
    path("healthz", healthz),
    path("v1/", include("orders.urls")),
    path("admin/", admin.site.urls),
]

# Serve static (DRF CSS/JS) in DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
