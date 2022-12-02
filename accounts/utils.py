from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
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
Create a dynamic for both email verification and password reset
"""
def send_email_verification(request, user, subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    # subject = 'Email Activation'
    
    """Create a context dictionary and pass in the data to be sent to the email verification file. The uid is the encoded version of a users primary key."""
    
    message = render_to_string(email_template,{
        'user':user,
        'domain': current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(subject, message, from_email, to= [to_email])
    mail.send()
    
    
# def send_password_reset_email(request, user):
#     from_email = settings.DEFAULT_FROM_EMAIL
#     current_site = get_current_site(request)
#     subject = 'Password Reset'
    
#     message = render_to_string('accounts/emails/reset_password_email.html',{
#         'user':user,
#         'domain': current_site,
#         'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': default_token_generator.make_token(user),
#     })
#     to_email = user.email
#     mail = EmailMessage(subject, message, from_email, to= [to_email])
#     mail.send() 
    
        