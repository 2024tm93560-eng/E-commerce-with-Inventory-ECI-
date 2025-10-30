from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from decimal import Decimal, InvalidOperation
import csv

from catalog.models import Product

TRUE_WORDS = {"1","true","yes","y","t"}
FALSE_WORDS = {"0","false","no","n","f",""}

def to_bool(val):
    if val is None:
        return True  # default to active if missing
    s = str(val).strip().lower()
    if s in TRUE_WORDS:  return True
    if s in FALSE_WORDS: return False
    return True

def to_decimal(val, rowno):
    s = str(val).strip() if val is not None else "0"
    s = s.replace(",", ".")
    try:
        d = Decimal(s)
    except (InvalidOperation, ValueError):
        raise CommandError(f"Row {rowno}: invalid price '{val}'")
    if d < 0:
        raise CommandError(f"Row {rowno}: price must be >= 0 (got {d})")
    return d

class Command(BaseCommand):
    help = "Import/Upsert products from CSV. Headers: sku,name,category,price,is_active"

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Path to CSV file")

    @transaction.atomic
    def handle(self, *args, **opts):
        path = opts["csv_path"]
        created = updated = skipped = 0

        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if not reader.fieldnames:
                    raise CommandError("CSV has no header row.")

                headers = [h.strip().lower() for h in reader.fieldnames]
                required = {"sku","name","category","price","is_active"}
                missing = required - set(headers)
                if missing:
                    raise CommandError(f"CSV missing required columns: {missing}")

                for i, raw in enumerate(reader, start=2):
                    row = {k.strip().lower(): (v or "") for k, v in raw.items()}

                    sku = row["sku"].strip()
                    if not sku:
                        skipped += 1
                        continue

                    name = row["name"].strip()
                    category = row["category"].strip()
                    price = to_decimal(row["price"], i)
                    is_active = to_bool(row["is_active"])

                    obj, was_created = Product.objects.update_or_create(
                        sku=sku,
                        defaults={
                            "name": name,
                            "category": category,
                            "price": price,
                            "is_active": is_active,
                        }
                    )
                    if was_created:
                        created += 1
                    else:
                        updated += 1

        except FileNotFoundError:
            raise CommandError(f"File not found: {path}")

        self.stdout.write(self.style.SUCCESS(
            f"Import OK. Created: {created}, Updated: {updated}, Skipped(blank sku): {skipped}"
        ))
