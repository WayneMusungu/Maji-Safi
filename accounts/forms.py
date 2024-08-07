from django import forms
from .models import User, UserProfile
from .validators import allow_only_images_valdators
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import re

def validate_special_character(value):
    # This is a custom validator that adds aditional layer of complexity to ensure passwords
    # includes characters beyond alpha numeric ones
    pattern = r'[\W_]+'
    if not re.search(pattern, value):
        raise ValidationError('Password must contain at least one special character eg."~!@#$%^&*"')

class UserForm(forms.ModelForm):
    # validate_password ensures that the password meets Django's default password strength requirements
    password = forms.CharField(widget=forms.PasswordInput(), validators=[validate_password, validate_special_character])
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords do not match!!')

        return confirm_password

    def clean_email(self):
        email = self.cleaned_data['email']
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise forms.ValidationError("Enter a valid email address.")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email address already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with this username already exists.")
        return username

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_valdators])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_valdators])

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'county', 'town', 'pin_code']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        
        
class ChangePasswordForm(forms.Form):
    otp = forms.CharField(label='OTP')
    new_password = forms.CharField(widget=forms.PasswordInput(), label='New Password', validators=[validate_password, validate_special_character])
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirm New Password')

    def clean(self):
        # This method is called to clean and validate the form fields
        # It ensures all the fields are properly cleaned and validated before
        # custom logic is applied
        cleaned_data = super().clean() # Call the parent class's clean method to get the cleaned data
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise ValidationError("New passwords do not match!")

        return cleaned_data
    

class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(), label='New Password', validators=[validate_password, validate_special_character])
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirm New Password')

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise ValidationError("New passwords do not match!")
        
        return cleaned_data
