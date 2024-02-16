from django.test import TestCase
from django.db.utils import IntegrityError
from marketplace.models import Tax
from decimal import Decimal  


class TaxModelTest(TestCase):
    def setUp(self):
        Tax.objects.create(tax_type='VAT', tax_percentage='10.00', is_active=True)
        Tax.objects.create(tax_type='Sales Tax', tax_percentage='5.50', is_active=False)

    def test_tax_str_method(self):
        vat_tax = Tax.objects.get(tax_type='VAT')
        sales_tax = Tax.objects.get(tax_type='Sales Tax')

        self.assertEqual(str(vat_tax), 'VAT')
        self.assertEqual(str(sales_tax), 'Sales Tax')

    def test_tax_unique_constraint(self):
        # Attempt to create a tax with the same tax_type, should raise IntegrityError
        with self.assertRaises(IntegrityError):
            Tax.objects.create(tax_type='VAT', tax_percentage='15.00', is_active=True)

    def test_tax_percentage_decimal_places(self):
        vat_tax = Tax.objects.get(tax_type='VAT')
        
        # Convert the Decimal to string for comparison
        expected_percentage = Decimal('10.00').quantize(Decimal('0.00'))
        self.assertEqual(vat_tax.tax_percentage, expected_percentage)


    def test_tax_is_active_default_value(self):
        sales_tax = Tax.objects.get(tax_type='Sales Tax')
        self.assertFalse(sales_tax.is_active)
