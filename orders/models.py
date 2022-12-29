from django.db import models
from accounts.models import User

# Create your models here.

class Payment(models.Model):
    PAYMENT_METHOD = (
        ('MPESA', 'MPESA'),
        ('Paypal', 'Paypal')
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=100)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.transaction_id

