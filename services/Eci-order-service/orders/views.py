import logging
import requests 
from typing import Any, Dict, List

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import Order, OrderItem
from .serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderItemSerializer,
)
from .services import OrderService
from .mq import publish_order_confirmed  # <-- use the mq.py publisher

log = logging.getLogger(__name__)


def _build_event_payload(d: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build the event payload expected by the notification worker.
    Emits snake_case keys inside an 'order' object so the email template fills.
    """
    items_in: List[Dict[str, Any]] = d.get("items", []) or []
    items_out = []
    for it in items_in:
        items_out.append({
            "sku":         it.get("sku"),
            "name":        it.get("product_name") or it.get("name"),
            "qty":         it.get("quantity") or it.get("qty"),
            "unit_price":  it.get("unit_price") or it.get("price") or it.get("unit"),
            "total":       it.get("line_total") or it.get("amount_total") or it.get("total"),
        })

    order_id       = d.get("order_id") or d.get("number") or d.get("id")
    customer_email = d.get("customer_email")
    customer_name  = d.get("customer_name") or "Customer"
    currency       = d.get("currency") or d.get("currency_code") or "QAR"

    payload: Dict[str, Any] = {
        "to": customer_email,
        "customer": {"email": customer_email, "name": customer_name},
        "order": {
            "id":        order_id,
            "currency":  currency,
            "items":     items_out,
            "subtotal":  d.get("subtotal"),
            "tax":       d.get("tax"),
            "shipping":  d.get("shipping"),
            "total":     d.get("order_total") or d.get("total"),
        },
        "idempotency_key": d.get("idempotency_key") or order_id,
        "order_status":    d.get("order_status"),
    }

    return payload


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Order operations.
    """
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["order_status", "payment_status", "customer_id"]
    ordering_fields = ["created_at", "order_total"]

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderSerializer

    def create(self, request):
        """
        Create a new order with inventory reservation and idempotency support.
        Publishes an 'order.confirmed' style event after successful creation.
        """
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        idempotency_key = request.headers.get("Idempotency-Key")
        items = serializer.validated_data["items"]

        # Step 1: Lookup product details by SKU
product_response = requests.get(f"http://inventory-app:8000/v1/products/by-sku/{item['sku']}")
if product_response.status_code != 200:
    logger.error(f"Failed to fetch product for SKU {item['sku']}")
    return Response({"error": "Product lookup failed"}, status=status.HTTP_400_BAD_REQUEST)

product = product_response.json()

# Step 2: Build reserve payload
reserve_payload = {
    "product_id": product["id"],
    "warehouse": product["default_warehouse"],
    "quantity": item["quantity"],
    "idempotency_key": f"{order_id}-{item['sku']}"
}

# Step 3: Reserve inventory
reserve_response = requests.post(
    "http://inventory-app:8000/v1/reserve_inventory",
    json=reserve_payload
)

if reserve_response.status_code != 200:
    logger.error(f"Inventory reservation failed: {reserve_response.text}")
    return Response({"error": "Inventory reservation failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """Cancel an order."""
        order = self.get_object()
        try:
            cancelled_order = OrderService.cancel_order(order)
            serializer = OrderSerializer(cancelled_order)
            return Response(serializer.data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def confirm(self, request, pk=None):
        """Manually confirm an order and publish the event."""
        order = self.get_object()

        if order.order_status != "PENDING":
            return Response(
                {"error": "Only pending orders can be confirmed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order.order_status = "CONFIRMED"
        order.save(update_fields=["order_status"])

        serializer = OrderSerializer(order)
        d = serializer.data
        payload = _build_event_payload(d)

        try:
            publish_order_confirmed(payload)
            log.info(
                "order.confirm.publish.ok",
                extra={"order_id": d.get("order_id"), "to": payload.get("to")},
            )
        except Exception:
            log.exception("order.confirm.publish.failed")

        return Response(d, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def items(self, request, pk=None):
        """Get items for a specific order."""
        order = self.get_object()
        items = order.items.all()
        serializer = OrderItemSerializer(items, many=True)
        return Response(serializer.data)
    


def get_product_details(sku):
    try:
        response = requests.get(f"http://inventory:8000/v1/products/by-sku/{sku}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Failed to fetch product details for SKU {sku}: {str(e)}")
        return None

