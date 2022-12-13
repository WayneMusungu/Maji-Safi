from django.db import models
from supplier.models import Supplier

# Create your models here.

class Type(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    # bottle_size = models.CharField(max_length=50, unique=True)
    water_type = models.CharField(max_length=50)
    """
    A slug field in Django is used to store and generate valid URLs for your dynamically created web pages.
    """
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # class Meta:
    #     verbose_name = 'child'
    #     verbose_name_plural = "children"
    class Meta:
        ordering = ('-created_at',)
    
    """
    Capitalize the name of the water type
    """
    def clean(self):
        self.water_type = self.water_type.capitalize()
    
    def __str__(self):
        return self.water_type
    
class Product(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='products')
    bottle_size = models.CharField(max_length=50)
    # water_type = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100)
    description = models.TextField(max_length=250, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='waterimages')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at', '-created_at']
        # ordering = ('-created_at',)
    
    def __str__(self):
        return f'{self.bottle_size}, for {self.price} ksh'
    


