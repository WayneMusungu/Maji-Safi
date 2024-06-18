from django.contrib.sites.shortcuts import get_current_site
from accounts.tasks import send_email_verification_task, send_notification_task
"""
This file will contain any helper function for myAccount
"""

def detectUser(user):
    if user.role == 1:
        redirectUrl = 'supplierDashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'customerDashboard'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl
    
def send_email_verification(request, user, subject, email_template):
    current_site = get_current_site(request).domain
    send_email_verification_task.delay(user.id, subject, email_template, current_site)

def send_notification(subject, email_template, context):
    send_notification_task.delay(subject, email_template, context)
             