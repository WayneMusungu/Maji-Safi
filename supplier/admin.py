from django.contrib import admin

from supplier.models import Supplier

# Register your models here.

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('user', 'supplier_name', 'is_approved', 'created_at')
    list_display_links = ('user', 'supplier_name')
    list_editable = ('is_approved',)
    

admin.site.register(Supplier, SupplierAdmin)
