from django import forms
from .models import Order
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

class OrderForm(forms.ModelForm):
    phone = PhoneNumberField(
        widget = PhoneNumberPrefixWidget(initial='KE')
    )
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address', 'country', 'county', 'town', 'pin_code']