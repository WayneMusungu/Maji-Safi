from django.contrib import admin
from .models import Category, Product

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'bottle_size', 'updated_at')
    prepopulated_fields = {'slug': ('bottle_size',)}
    search_fields = ('bottle_size', 'supplier__supplier_name')
    
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ('water_type', 'category', 'supplier', 'price', 'is_available', 'updated_at')
    prepopulated_fields = {'slug': ('water_type',)}
    search_fields = ('water_type', 'category__bottle_size', 'supplier__supplier_name', 'price')
    list_filter = ('is_available',)

    

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)

