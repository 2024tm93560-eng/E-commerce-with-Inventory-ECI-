from django.db import transaction
from inventory.models import Inventory

@transaction.atomic
def reserve_inventory(product_id, warehouse, quantity):
    inv = Inventory.objects.select_for_update().get(product_id=product_id, warehouse=warehouse)
    if inv.on_hand - inv.reserved >= quantity:
        inv.reserved += quantity
        inv.save()
        return True
    return False
