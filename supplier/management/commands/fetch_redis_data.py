import redis
import pickle
import re
from django.core.management.base import BaseCommand
from django.core.cache import cache
from orders.models import Order, OrderedProduct
from supplier.models import Supplier

class Command(BaseCommand):
    help = 'Fetch and print data stored in Redis'

    def add_arguments(self, parser):
        parser.add_argument('--fetch', nargs=2, metavar=('USERNAME', 'SUPPLIER_ID'), help='Fetch data for a specific username and supplier_id')
        parser.add_argument('--order', type=str, help='Fetch order details for a specific order number')

    def handle(self, *args, **kwargs):
        r = redis.StrictRedis(host='127.0.0.1', port=6379, db=1)

        # List all keys in the current Redis database
        keys = r.keys('*')
        self.stdout.write(self.style.SUCCESS(f"All keys: {keys}"))

        if kwargs['fetch']:
            username, supplier_id = kwargs['fetch']
            cache_key = f':1:my_orders_{username}_{supplier_id}'

            if cache_key.encode('utf-8') not in keys:
                self.stdout.write(self.style.WARNING("Specified key not found in the current database"))
                return

            # Fetch the cached value
            cached_value = r.get(cache_key)

            if cached_value:
                try:
                    deserialized_value = pickle.loads(cached_value)
                    self.stdout.write(self.style.SUCCESS(f"Cached value: {deserialized_value}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error deserializing value: {e}"))
            else:
                self.stdout.write(self.style.WARNING("Key not found or value is None"))

        elif kwargs['order']:
            order_number = kwargs['order']
            cache_key = f'order_detail_{order_number}'
            cached_value = cache.get(cache_key)

            if cached_value:
                self.stdout.write(self.style.SUCCESS("Retrieving from cache"))
                self.stdout.write(self.style.SUCCESS(f"Cached value: {cached_value}"))
            else:
                self.stdout.write(self.style.SUCCESS("Retrieving from database"))
                try:
                    order = Order.objects.get(order_number=order_number, is_ordered=True)
                    ordered_product = OrderedProduct.objects.filter(order=order, productitem__supplier=Supplier.objects.get(user__username=kwargs['fetch'][0]))

                    context = {
                        'order': order,
                        'ordered_product': ordered_product,
                        'subtotal': order.get_total_by_supplier()['subtotal'],
                        'tax_data': order.get_total_by_supplier()['tax_dict'],
                        'grand_total': order.get_total_by_supplier()['grand_total'],
                    }
                    cache.set(cache_key, context, timeout=300)  # Cache timeout of 5 minutes
                    self.stdout.write(self.style.SUCCESS(f"Database value: {context}"))
                except Order.DoesNotExist:
                    self.stdout.write(self.style.ERROR("Order does not exist"))
        else:
            # If no specific key is requested, list all relevant keys
            pattern = re.compile(r':1:my_orders_(.+?)_(\d+)')
            relevant_keys = [key.decode('utf-8') for key in keys if pattern.match(key.decode('utf-8'))]
            
            self.stdout.write(self.style.SUCCESS(f"Relevant keys: {relevant_keys}"))
            self.stdout.write(self.style.WARNING("Use the --fetch option with username and supplier_id to fetch specific data."))
