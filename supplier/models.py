from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification
from datetime import time, date, datetime



# # Create your models here.

class Supplier(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    supplier_name = models.CharField(max_length=45)
    supplier_slug = models.CharField(max_length=100, unique=True)
    supplier_license = models.ImageField(upload_to='supplier/license')
    qr_code = models.ImageField(upload_to='supplier/qr_codes')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.supplier_name
    
    def is_open(self):
        """
        Check current day's opening hours
        """
        today_date = date.today()
        today = today_date.isoweekday()
        
        current_opening_hours = OpeningHour.objects.filter(supplier=self, day=today)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        """
        Check if there is multiple opening hours in the same day and determine whether the water shop is opened/closed during a specific time frame
        """
                
        is_open = None
        for current in current_opening_hours:
            if not current.is_closed:
                start = str(datetime.strptime(current.from_hour, "%I:%M %p").time())
                end = str(datetime.strptime(current.to_hour, "%I:%M %p").time())
        
                if current_time > start and current_time < end:
                    is_open = True
                    break
                else:
                    is_open = False
        return is_open

    
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
                    'is_approved': self.is_approved,
                    # Explicitly assign the to_email
                    'to_email': self.user.email,
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
    
 
DAYS = [
    (1, ("Monday")),
    (2, ("Tuesday")),
    (3, ("Wednesday")),
    (4, ("Thursday")),
    (5, ("Friday")),
    (6, ("Saturday")),
    (7, ("Sunday")),  
]


HOUR_OF_DAY_24 = [(time(h,m).strftime('%I:%M %p'), time(h,m).strftime('%I:%M %p')) for h in range(0, 24) for m in (0, 30)]
    
class OpeningHour(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    to_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    is_closed = models.BooleanField(default=False)
    
    
    class Meta:
        ordering = ('day', 'from_hour')
        unique_together = ('supplier', 'day', 'from_hour', 'to_hour')
        
    def __str__(self):
        return self.get_day_display()