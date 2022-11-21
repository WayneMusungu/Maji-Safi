from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification

# # Create your models here.

class Supplier(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    supplier_name = models.CharField(max_length=45)
    supplier_slug = models.CharField(max_length=100, unique=True)
    supplier_license = models.ImageField(upload_to='supplier/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.supplier_name
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            #Update
            """
            Get the status of the Supplier if they are approved or not
            """
            original_status = Supplier.objects.get(pk=self.pk)
            if original_status.is_approved != self.is_approved:
                email_template = 'accounts/emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved
                }
                if self.is_approved == True:
                    # Send notification email that their account has been approved to post their water business
                    """
                    Create a helper function to send emails
                    """
                    subject = 'Congrats!! Your Water Shop Business has been approved'
                    send_notification(subject, email_template, context)
                else:
                    subject = 'Sorry you are not eligible to register your Water Shop Business'
                    # Send notification email that their account has not been approved to post their water business
                    send_notification(subject, email_template, context)
           
        """
        The super function allows you to access the save method of the Supplier class
        """
        return super(Supplier, self).save(*args, **kwargs)
