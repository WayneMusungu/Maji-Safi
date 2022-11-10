from django import forms
from .models import Supplier

class SupplierForm(forms.ModelForm):
    supplier_license = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}))

    class Meta:
        model = Supplier
        fields = ['supplier_name', 'supplier_license']