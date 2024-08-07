from django.db import models
from accounts.models import User
from services.models import Product
from django_countries.fields import CountryField
from supplier.models import Supplier
import simplejson as json


request_object = ''

# Create your models here.

class Payment(models.Model):
    PAYMENT_METHOD = (
        ('MPESA', 'MPESA'),
        ('Paypal', 'Paypal'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=100)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.transaction_id
    

class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    suppliers = models.ManyToManyField(Supplier, blank=True)
    order_number = models.CharField(max_length=20) #To generate order_number take the current date time and concatenate it with the pk
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=200)
    country = CountryField(blank_label='(select country)')
    county = models.CharField(max_length=15, blank=True)
    town = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    total = models.FloatField()
    tax_data = models.JSONField(blank=True, help_text = "Data format: {'tax_type':{'tax_percentage':'tax_amount'}}")
    total_data = models.JSONField(blank=True, null=True)
    total_tax = models.FloatField()
    payment_method = models.CharField(max_length=25)
    status = models.CharField(max_length=15, choices=STATUS, default='New')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'
    
    def ordered_placed_to(self):
        return ", ".join([str(i) for i in self.suppliers.all()])
    
    # Create a custom middleware to access the request object in orders.models.py
    def get_total_by_supplier(self):
        supplier = Supplier.objects.get(user=request_object.user)
        
        subtotal = 0
        tax = 0
        tax_dict = {}
        
        if self.total_data:
            total_data = json.loads(self.total_data)
            data = total_data.get(str(supplier.id))
            # print(data)
            
            for key, val in data.items():
                subtotal += float(key)
                val = val.replace("'", '"')
                # print(val)
                val = json.loads(val)
                tax_dict.update(val)
            # print(subtotal)
            # print(tax_dict)
            
            
            # Calculate tax
            # {"Excise-Duty": {"3.50": "1.40"}, "Delivery": {"0.25": "0.10"}}
            for i in val:
                print(i)
                for j in val[i]:
                    # print(val[i][j])
                    tax += float(val[i][j])
        
        grand_total = float(subtotal) + float(tax)
        # print('subtotal==>', subtotal)
        # print('tax==>', tax)
        # print('tax_dict==>', tax_dict)
        # print('grand_total==>', grand_total)
        context = {
            'subtotal':subtotal,
            'tax_dict': tax_dict,
            'grand_total': grand_total
        }
        return context

    def __str__(self):
        return self.order_number
    
    
class OrderedProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    productitem = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.productitem.bottle_size

    
    

