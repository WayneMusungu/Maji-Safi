from django import forms
from .models import User, UserProfile
from .validators import allow_only_images_valdators
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import re

def validate_special_character(value):
    pattern = r'[\W_]+'
    if not re.search(pattern, value):
        raise ValidationError('Password must contain at least one special character eg."~!@#$%^&*"')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), validators=[validate_password, validate_special_character])
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean(self):
        """
        The super function give us the ability to overide
        the clean method which is an inbuilt function
        """
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Passwords do not match!!'
            )

class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'start typing .....', 'required':'required'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_valdators])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_valdators])

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'country', 'county', 'town', 'address', 'pin_code']


class UserInfoForm(forms.ModelForm):
    phone_number = PhoneNumberField(
        widget = PhoneNumberPrefixWidget(initial='KE')
    )

    class Meta:

        model = User
        fields = ['first_name', 'last_name', 'phone_number']