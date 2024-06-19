from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from accounts.tasks import send_email_verification_task

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
    
"""
Function to send notification to Supplier if their business has been approved by the admin or not
"""
def send_notification(subject, email_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(email_template, context)
    # to_email = context['user'].email  => Logged in user's email address
    if(isinstance(context['to_email'], str)): # check if the email address is str or not
        to_email = []
        to_email.append(context['to_email'])
    else:
        to_email = to_email = context['to_email']  # Explicitly assign to_email to the Supplier models    
    mail = EmailMessage(subject, message, from_email, to= to_email)
    mail.content_subtype = 'html'
    mail.send()
    

def send_email_verification(request, user, subject, email_template):
    current_site = get_current_site(request).domain
    send_email_verification_task.delay(user.id, subject, email_template, current_site)

