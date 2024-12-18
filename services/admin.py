from django.contrib import admin
from .models import Type, Product

# Register your models here.

class TypeAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'water_type', 'updated_at')
    prepopulated_fields = {'slug': ('water_type',)}
    search_fields = ('water_type', 'supplier__supplier_name')
    
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ('bottle_size', 'type', 'supplier', 'price', 'is_available', 'updated_at')
    search_fields = ('bottle_size', 'type__water_type', 'supplier__supplier_name', 'price')
    list_filter = ('is_available',)

    

admin.site.register(Type, TypeAdmin)
admin.site.register(Product, ProductAdmin)