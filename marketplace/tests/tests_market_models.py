from django.test import TestCase
from django.db.utils import IntegrityError
from marketplace.models import Tax

class TaxModelTest(TestCase):
    def setUp(self):
        # Set up test data
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
        self.assertEqual(vat_tax.tax_percentage, 10.00) 

    def test_tax_is_active_default_value(self):
        sales_tax = Tax.objects.get(tax_type='Sales Tax')
        self.assertFalse(sales_tax.is_active)
