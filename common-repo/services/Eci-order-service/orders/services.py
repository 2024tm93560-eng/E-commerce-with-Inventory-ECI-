# orders/services.py
import csv
import uuid
import logging
from decimal import Decimal
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from django.conf import settings
from django.db import transaction

log = logging.getLogger(__name__)


# ----------------------------- CSV Utilities ----------------------------------
class CSVDataLoader:
    """Utility to load data from CSV files."""

    @staticmethod
    def get_csv_path(filename: str) -> Path:
        """Get path to CSV file in seed_data folder."""
        return Path(settings.BASE_DIR) / "seed_data" / filename

    @staticmethod
    def load_csv_to_dict(filename: str, key_field: str = "id") -> Dict:
        """Load CSV file into dict keyed by specified field."""
        csv_path = CSVDataLoader.get_csv_path(filename)
        data: Dict = {}

        if not csv_path.exists():
            log.warning("csv.missing_file: %s", csv_path)
            return data

        try:
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    raw_key = row.get(key_field)
                    if raw_key is None:
                        continue
                    key = int(raw_key) if str(raw_key).isdigit() else raw_key
                    data[key] = row
            log.info("csv.loaded: file=%s count=%d", filename, len(data))
        except Exception:
            log.exception("csv.load_failed: %s", filename)

        return data

    @staticmethod
    def load_csv_to_list(filename: str) -> List[Dict]:
        """Load CSV file into list of dicts."""
        csv_path = CSVDataLoader.get_csv_path(filename)
        data: List[Dict] = []

        if not csv_path.exists():
            log.warning("csv.missing_file: %s", csv_path)
            return data

        try:
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                data.extend(reader)
            log.info("csv.loaded: file=%s count=%d", filename, len(data))
        except Exception:
            log.exception("csv.load_failed: %s", filename)

        return data


# ----------------------------- Mock Services ----------------------------------
class MockCustomerService:
    """Mock Customer Service backed by eci_customers.csv"""
    CUSTOMERS: Dict[int, Dict] = {}

    @classmethod
    def load_from_csv(cls, filename: str = "eci_customers.csv") -> None:
        cls.CUSTOMERS = CSVDataLoader.load_csv_to_dict(filename, key_field="customer_id")
        # Normalize
        for customer_id, c in list(cls.CUSTOMERS.items()):
            cls.CUSTOMERS[customer_id] = {
                "customer_id": int(c["customer_id"]),
                "name": c["name"],
                "email": c["email"],
                "phone": c.get("phone", ""),
                "created_at": c.get("created_at", ""),
            }

    @classmethod
    def get_customer(cls, customer_id: int) -> Optional[Dict]:
        if not cls.CUSTOMERS:
            cls.load_from_csv()
        return cls.CUSTOMERS.get(customer_id)


class MockCatalogService:
    """Mock Catalog Service backed by eci_products.csv"""
    PRODUCTS: Dict[int, Dict] = {}

    @classmethod
    def load_from_csv(cls, filename: str = "eci_products.csv") -> None:
        cls.PRODUCTS = CSVDataLoader.load_csv_to_dict(filename, key_field="product_id")
        # Normalize
        for product_id, p in list(cls.PRODUCTS.items()):
            is_active_str = str(p.get("is_active", "True")).lower()
            is_active = is_active_str in ("true", "1", "yes")
            cls.PRODUCTS[product_id] = {
                "product_id": int(p["product_id"]),
                "sku": p["sku"],
                "name": p["name"],
                "category": p.get("category", ""),
                "price": Decimal(str(p["price"])),
                "is_active": is_active,
            }

    @classmethod
    def get_product(cls, product_id: int) -> Optional[Dict]:
        if not cls.PRODUCTS:
            cls.load_from_csv()
        return cls.PRODUCTS.get(product_id)

    @classmethod
    def get_product_by_sku(cls, sku: str) -> Optional[Dict]:
        if not cls.PRODUCTS:
            cls.load_from_csv()
        for product in cls.PRODUCTS.values():
            if product["sku"] == sku:
                return product
        return None


class MockInventoryService:
    """Mock Inventory Service backed by eci_inventory.csv"""
    INVENTORY: Dict[str, Dict] = {}

    @classmethod
    def load_from_csv(cls, filename: str = "eci_inventory.csv") -> None:
        inventory_list = CSVDataLoader.load_csv_to_list(filename)
        cls.INVENTORY = {}
        for item in inventory_list:
            product_id = int(item["product_id"])
            warehouse = item["warehouse"]
            key = f"{product_id}-{warehouse}"
            cls.INVENTORY[key] = {
                "inventory_id": int(item["inventory_id"]),
                "product_id": product_id,
                "warehouse": warehouse,
                "on_hand": int(item["on_hand"]),
                "reserved": int(item.get("reserved", 0)),
                "updated_at": item.get("updated_at", ""),
            }

    @classmethod
    def get_inventory(cls, product_id: int, warehouse: Optional[str] = None):
        if not cls.INVENTORY:
            cls.load_from_csv()

        if warehouse:
            key = f"{product_id}-{warehouse}"
            return cls.INVENTORY.get(key)

        return [inv for inv in cls.INVENTORY.values() if inv["product_id"] == product_id]

    @classmethod
    def check_availability(cls, product_id: int, quantity: int, warehouse: Optional[str] = None) -> Tuple[bool, Optional[str]]:
        if not cls.INVENTORY:
            cls.load_from_csv()

        if warehouse:
            inv = cls.get_inventory(product_id, warehouse)
            if inv:
                available = inv["on_hand"] - inv["reserved"]
                return available >= quantity, warehouse
        else:
            for inv in cls.get_inventory(product_id):
                available = inv["on_hand"] - inv["reserved"]
                if available >= quantity:
                    return True, inv["warehouse"]

        return False, None

    @classmethod
    def reserve_stock(cls, product_id: int, sku: str, quantity: int) -> Dict:
        if not cls.INVENTORY:
            cls.load_from_csv()

        ok, warehouse = cls.check_availability(product_id, quantity)
        if ok:
            return {
                "success": True,
                "reservation_id": f"RES-{uuid.uuid4().hex[:12]}",
                "warehouse": warehouse,
                "quantity": quantity,
            }
        return {"success": False, "error": f"Insufficient stock for product {product_id}"}

    @classmethod
    def release_reservation(cls, reservation_id: str) -> Dict:
        # Mock release always succeeds
        return {"success": True, "released": reservation_id}


class MockPaymentService:
    """Mock Payment Service - simple simulation."""

    @staticmethod
    def charge(order_id, amount: Decimal, idempotency_key: str) -> Dict:
        # Always succeeds in mock
        return {
            "success": True,
            "payment_id": f"PAY-{uuid.uuid4().hex[:12]}",
            "amount": amount,
            "status": "PAID",
        }

    @staticmethod
    def refund(payment_id: str, amount: Decimal) -> Dict:
        # Always succeeds in mock
        return {
            "success": True,
            "refund_id": f"REF-{uuid.uuid4().hex[:12]}",
            "amount": amount,
            "status": "REFUNDED",
        }


# ------------------------------ Order Service ---------------------------------
class OrderService:
    """
    Business logic for order operations.
    Pure domain behavior; no messaging here (publisher lives in mq.py, called by views).
    """

    # Wire mock integrations (swap with real clients later if needed)
    CustomerService = MockCustomerService
    CatalogService = MockCatalogService
    InventoryService = MockInventoryService
    PaymentService = MockPaymentService

    @staticmethod
    @transaction.atomic
    def create_order(
        customer_id: int,
        items_data: List[Dict],
        idempotency_key: Optional[str] = None,
        shipping: Decimal = Decimal("10.00"),
    ):
        """
        Create a new order with reservation + payment workflow.
        Returns: (order, created: bool)
        """
        from .models import Order, OrderItem  # local import to avoid circulars

        # Idempotency
        if idempotency_key:
            existing = Order.objects.filter(idempotency_key=idempotency_key).first()
            if existing:
                log.info("order.idempotent_hit: key=%s order_id=%s", idempotency_key, existing.order_id)
                return existing, False

        # Customer lookup
        customer_info = OrderService.CustomerService.get_customer(customer_id)
        if not customer_info:
            raise ValueError(f"Customer {customer_id} not found")

        # Create order (PENDING/UNPAID)
        order = Order.objects.create(
            customer_id=customer_id,
            customer_name=customer_info["name"],
            customer_email=customer_info["email"],
            idempotency_key=idempotency_key,
            shipping=shipping,
            order_status="PENDING",
            payment_status="UNPAID",
        )

        # Create lines + reserve inventory
        reservations: List[str] = []
        try:
            for item in items_data:
                product = OrderService.CatalogService.get_product(item["product_id"])
                if not product:
                    raise ValueError(f"Product {item['product_id']} not found")

                if not product.get("is_active", True):
                    raise ValueError(f"Product {product['name']} is not active")

                res = OrderService.InventoryService.reserve_stock(
                    product_id=product["product_id"],
                    sku=product["sku"],
                    quantity=item["quantity"],
                )
                if not res.get("success"):
                    raise ValueError(f"Cannot reserve {product['name']}: {res.get('error', 'Insufficient stock')}")

                reservations.append(res["reservation_id"])

                line = OrderItem.objects.create(
                    order=order,
                    product_id=product["product_id"],
                    sku=product["sku"],
                    product_name=product["name"],
                    quantity=item["quantity"],
                    unit_price=product["price"],
                    reservation_id=res["reservation_id"],
                    warehouse=res["warehouse"],
                )
                line.calculate_line_total()
                line.save()

            # Totals
            order.calculate_totals()
            order.save()

            # Payment
            pay = OrderService.PaymentService.charge(
                order_id=order.order_id,
                amount=order.order_total,
                idempotency_key=idempotency_key or str(uuid.uuid4()),
            )
            if not pay.get("success"):
                raise ValueError("Payment failed")

            order.order_status = "CONFIRMED"
            order.payment_status = "PAID"
            order.save()

            log.info("order.created_ok: order_id=%s total=%s", order.order_id, order.order_total)
            return order, True

        except Exception:
            # Rollback helpers: release any reservations we made
            for res_id in reservations:
                try:
                    OrderService.InventoryService.release_reservation(res_id)
                except Exception:
                    log.warning("inventory.release_failed: reservation_id=%s", res_id, exc_info=True)
            # If we created an order, let the transaction rollback delete it if needed
            log.exception("order.create_failed")
            raise

    @staticmethod
    @transaction.atomic
    def cancel_order(order):
        """
        Cancel an order (release reservations, refund if paid).
        """
        if order.order_status == "CANCELLED":
            return order
        if order.order_status == "DELIVERED":
            raise ValueError("Cannot cancel delivered order")

        # Release reservations
        for item in order.items.all():
            if item.reservation_id:
                try:
                    OrderService.InventoryService.release_reservation(item.reservation_id)
                except Exception:
                    log.warning("inventory.release_failed: reservation_id=%s", item.reservation_id, exc_info=True)

        # Refund if paid
        if order.payment_status == "PAID":
            try:
                OrderService.PaymentService.refund(f"PAY-{order.order_id}", order.order_total)
                order.payment_status = "REFUNDED"
            except Exception:
                log.exception("payment.refund_failed")
                raise

        order.order_status = "CANCELLED"
        order.save()

        log.info("order.cancelled_ok: order_id=%s", order.order_id)
        return order
