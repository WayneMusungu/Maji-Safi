import qrcode
from io import BytesIO
from django.core.files import File
from django.core.management.base import BaseCommand
from supplier.models import Supplier
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils.text import slugify 


class Command(BaseCommand):
    help = 'Generate or replace QR codes for all suppliers'

    def handle(self, *args, **kwargs):
        # Determine if the app is running locally or in production
        if settings.DEBUG:
            domain = 'localhost:8000'  # Localhost URL for development
        else:
            current_site = Site.objects.get_current()
            domain = current_site.domain  # Use actual domain in production

        # Fetch all suppliers
        suppliers = Supplier.objects.all()

        for supplier in suppliers:
            try:
                # Generate the QR code for the supplier's detail page URL
                supplier_detail_url = f'http://{domain}/marketplace/{supplier.supplier_slug}/'
                qr_image = qrcode.make(supplier_detail_url)
                
                # Save the QR code image to a BytesIO buffer
                buffer = BytesIO()
                qr_image.save(buffer, format='PNG')

                # Reset the buffer's position to the beginning
                buffer.seek(0)

                # Format the file name to include slug and '_qr_code.png'
                file_name = f'{slugify(supplier.supplier_name)}_qr_code.png'

                # Save the QR code to the Supplier model
                supplier.qr_code.save(file_name, File(buffer), save=False)
                supplier.save()

                self.stdout.write(self.style.SUCCESS(f'Successfully generated/replaced QR code for supplier: {supplier.supplier_name}'))
            
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error generating QR code for supplier: {supplier.supplier_name}, Error: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('QR code generation process completed.'))
