from inventory.models import Inventory

def allocate_inventory(product_id, quantity):
    inventories = Inventory.objects.filter(product_id=product_id).order_by('-on_hand')
    for inv in inventories:
        available = inv.on_hand - inv.reserved
        if available >= quantity:
            return [{'warehouse': inv.warehouse, 'quantity': quantity}]
    
    allocations = []
    remaining = quantity
    for inv in inventories:
        available = inv.on_hand - inv.reserved
        if available > 0:
            alloc_qty = min(available, remaining)
            allocations.append({'warehouse': inv.warehouse, 'quantity': alloc_qty})
            remaining -= alloc_qty
            if remaining <= 0:
                break
    return allocations if remaining == 0 else None
