from django import forms
from .models import Supplier, OpeningHour
from accounts.models import User
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
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


class SupplierPhoneNumber(forms.ModelForm):
    phone_number = PhoneNumberField(
        widget = PhoneNumberPrefixWidget(initial='KE')
    )
    class Meta:
        model = User
        fields = ['phone_number']