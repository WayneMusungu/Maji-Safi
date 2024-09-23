from django.core.management.base import BaseCommand
from supplier.models import Supplier

class Command(BaseCommand):
    help = 'Remove QR codes from suppliers'

    def handle(self, *args, **kwargs):
        # Fetch all suppliers with a QR code
        suppliers_with_qr = Supplier.objects.exclude(qr_code='')

        for supplier in suppliers_with_qr:
            try:
                # Delete the QR code file if it exists
                if supplier.qr_code:
                    supplier.qr_code.delete(save=False)
                
                # Clear the qr_code field in the Supplier model
                supplier.qr_code = ''
                supplier.save()

                self.stdout.write(self.style.SUCCESS(f'Successfully removed QR code for supplier: {supplier.supplier_name}'))
            
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error removing QR code for supplier: {supplier.supplier_name}, Error: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('QR code removal process completed.'))
