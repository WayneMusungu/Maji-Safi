from django.contrib import admin
from .models import Category, Product

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'category_name', 'updated_at')
    prepopulated_fields = {'slug': ('category_name',)}
    search_fields = ('category_name', 'supplier__supplier_name')
    
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ('water_brand_title', 'category', 'supplier', 'price', 'is_available', 'updated_at')
    prepopulated_fields = {'slug': ('water_brand_title',)}
    search_fields = ('water_brand_title', 'category__category_name', 'supplier__supplier_name', 'price')
    list_filter = ('is_available',)

    

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)

