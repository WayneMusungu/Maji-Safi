import qrcode
from io import BytesIO
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from accounts.tasks import send_email_verification_task, send_otp_email_task

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


def send_otp(request, user, otp):
    subject = 'Your OTP Code'
    email_template = 'accounts/emails/otp_email.html'
    context = {
        'user_id': user.id,
        'first_name': user.first_name,
        'otp': otp,
        'domain': request.get_host(),
        'year': timezone.now().year,
    }
    send_otp_email_task.delay(user.id, subject, email_template, context)

  
def generate_qr_code(url, supplier_name):
    """
    Generates a QR code for a given URL and saves it as a file.
    
    Args:
        url (str): The URL to encode in the QR code.
        supplier_name (str): The name of the supplier used to generate the file name.

    Returns:
        tuple: (BytesIO buffer, filename) of the saved QR code image.
    """
    # Generate the QR code
    qr_image = qrcode.make(url)
    
    # Save the QR code image to a BytesIO buffer
    buffer = BytesIO()
    qr_image.save(buffer, format='PNG')
    buffer.seek(0)
    
    # Generate a file name for the QR code using the slugified supplier name
    file_name = f'{slugify(supplier_name)}_qr_code.png'
    
    return buffer, file_name