from django.contrib import admin
from .models import Payment, Order, OrderedProduct

# Register your models here.

admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderedProduct)
