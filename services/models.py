from django.db import models
from supplier.models import Supplier

# Create your models here.

class Category(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50, unique=True)
    """
    A slug field in Django is used to store and generate valid URLs for your dynamically created web pages.
    """
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.category_name
    
class Product(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    water_brand_title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=250, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='waterimages')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.water_brand_title
    


