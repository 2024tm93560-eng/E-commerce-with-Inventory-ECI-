# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer

def ping(request):
    return HttpResponse("catalog service is alive")

def health(request):
    return JsonResponse({"status":"Ok", "service":"cagalog"})

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # make URLs use sku instead of numeric id
    lookup_field = "sku"
    lookup_value_regex = "[^/]+"
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "is_active", "price"] #exact matches
    search_fields = ["sku", "name", "category"]
    ordering_fields = ["price", "created_at", "updated_at", "name"]
    ordering = ["-updated_at"]
