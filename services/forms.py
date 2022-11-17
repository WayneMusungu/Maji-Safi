from django import forms

from accounts.validators import allow_only_images_valdators
from .models import Product, Type

class WaterTypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['water_type', 'description']
        
        
class WaterProductForm(forms.ModelForm):
    bottle_size = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '1 Litre, 500-ml, 300-ml'}))
    price = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': '500 (Kenya Shillings)'}))
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}), validators=[allow_only_images_valdators])

    class Meta:
        model = Product
        fields = ['type', 'bottle_size', 'description', 'price', 'image', 'is_available']