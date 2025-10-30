from django.core.management.base import BaseCommand
from inventory.models import Product, Inventory
import csv
import os
from django.conf import settings
from django.utils.dateparse import parse_datetime

class Command(BaseCommand):
    help = 'Load all product and inventory data from CSV into the database'

    def handle(self, *args, **kwargs):
        csv_path = os.path.join(settings.BASE_DIR, 'inventory', 'data', 'eci_inventory.csv')
        try:
            with open(csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                print("CSV headers:", reader.fieldnames)

                for row in reader:
                    # Extract product fields
                    product_id = int(row['product_id'])
                    sku = row.get('sku', f'SKU-{product_id}')
                    name = row.get('name', f'Product {product_id}')
                    category = row.get('category', 'Uncategorized')
                    price = float(row.get('price', 0.0))

                    # Create or update Product
                    product, _ = Product.objects.update_or_create(
                        id=product_id,
                        defaults={
                            'sku': sku,
                            'name': name,
                            'category': category,
                            'price': price
                        }
                    )

                    # Extract inventory fields
                    warehouse = row['warehouse']
                    on_hand = int(row['on_hand'])
                    reserved = int(row['reserved'])
                    updated_at = parse_datetime(row['updated_at']) if row['updated_at'] else None

                    # Create or update Inventory
                    Inventory.objects.update_or_create(
                        product=product,
                        warehouse=warehouse,
                        defaults={
                            'on_hand': on_hand,
                            'reserved': reserved,
                            'updated_at': updated_at
                        }
                    )

                self.stdout.write(self.style.SUCCESS("✅ All 120 items imported successfully."))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("❌ CSV file not found."))
