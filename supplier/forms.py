from django import forms
from .models import Supplier, OpeningHour
from accounts.validators import allow_only_images_valdators

class SupplierForm(forms.ModelForm):
    supplier_license = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_valdators])

    class Meta:
        model = Supplier
        fields = ['supplier_name', 'supplier_license']


class OpeningHourForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ['day', 'from_hour', 'to_hour', 'is_closed']
