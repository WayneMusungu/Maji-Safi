from django import forms
from .models import Type

class WaterTypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['water_type', 'description']