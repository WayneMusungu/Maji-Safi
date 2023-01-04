from django.contrib import admin
from .models import Payment, Order, OrderedProduct

# Register your models here.

class OrderedProductInline(admin.TabularInline):
    model = OrderedProduct
    readonly_fields = ('order', 'payment', 'user', 'productitem', 'quantity', 'price', 'amount')
    extra = 0
    
class OrderedAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'name', 'email', 'total', 'payment_method', 'status', 'is_ordered']
    inlines = [OrderedProductInline]

admin.site.register(Payment)
admin.site.register(Order, OrderedAdmin)
admin.site.register(OrderedProduct)
