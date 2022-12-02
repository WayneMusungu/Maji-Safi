from django.db import models
from accounts.models import User, UserProfile

# # Create your models here.

class Supplier(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    supplier_name = models.CharField(max_length=45)
    supplier_license = models.ImageField(upload_to='supplier/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.supplier_name
