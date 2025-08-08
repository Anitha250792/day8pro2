import json
from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Import products from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The path to the JSON file containing product data')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']

        try:
            with open(json_file, 'r') as f:
                products = json.load(f)
        except Exception as e:
            self.stderr.write(f"Error reading JSON file: {e}")
            return

        created_count = 0
        for item in products:
            product, created = Product.objects.get_or_create(
                name=item['name'],
                defaults={
                    'price': item['price'],
                    'brand': item['brand'],
                    'is_available': item['is_available'],
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created product: {product.name}")
            else:
                self.stdout.write(f"Product already exists: {product.name}")

        self.stdout.write(self.style.SUCCESS(f"Import complete. {created_count} products added."))
