from django.core.management.base import BaseCommand
from inventory.models import InventoryMovement, Inventory
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Release expired reservations older than 15 minutes'

    def handle(self, *args, **kwargs):
        expiry_time = timezone.now() - timedelta(minutes=15)
        expired_moves = InventoryMovement.objects.filter(
            movement_type='RESERVE',
            created_at__lt=expiry_time
        )

        for move in expired_moves:
            try:
                inv = Inventory.objects.get(product=move.product, warehouse=move.warehouse)
                inv.reserved = max(0, inv.reserved - move.quantity)
                inv.save()
                move.movement_type = 'EXPIRED'
                move.save()
                self.stdout.write(self.style.SUCCESS(f"Released reservation for {move.product.sku} in {move.warehouse}"))
            except Inventory.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Inventory not found for move {move.id}"))
