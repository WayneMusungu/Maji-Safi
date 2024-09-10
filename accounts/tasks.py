import logging
from time import sleep
from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from accounts.models import User

logger = logging.getLogger(__name__)

"""
Create a dynamic function for both email verification and password reset
"""
@shared_task(name='accounts.tasks.send_email_verification_task')
def send_email_verification_task(user_id, subject, email_template, domain):
    logger.info(f"Starting email verification task for user_id: {user_id}")
    try:
        sleep(20)
        logger.info("Simulated delay completed")

        user = User.objects.get(pk=user_id)
        logger.info(f"User fetched: {user.email}")

        from_email = settings.DEFAULT_FROM_EMAIL
        logger.info(f"From email: {from_email}")

        message = render_to_string(email_template, {
            'user': user,
            'domain': domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        logger.info(f"Email message rendered for user {user.email}")

        to_email = user.email
        mail = EmailMessage(subject, message, from_email, to=[to_email])
        mail.content_subtype = 'html'  # send the HTML content inside the email
        mail.send()
        logger.info(f"Email verification sent to {to_email}")
    except Exception as e:
        logger.error(f"Error in email verification task: {e}")


@shared_task(name='accounts.tasks.send_otp_email_task')
def send_otp_email_task(user_id, subject, email_template, context):
    logger.info(f"Starting OTP email task for user_id: {user_id}")
    try:
        user = User.objects.get(pk=user_id)
        logger.info(f"User fetched: {user.email}")

        from_email = settings.DEFAULT_FROM_EMAIL
        logger.info(f"From email: {from_email}")

        message = render_to_string(email_template, context)
        logger.info(f"Email message rendered for user {user.email}")

        to_email = user.email
        mail = EmailMessage(subject, message, from_email, to=[to_email])
        mail.content_subtype = 'html'  # Send the HTML content inside the email
        mail.send()
        logger.info(f"OTP email sent to {to_email}")
    except Exception as e:
        logger.error(f"Error in OTP email task: {e}")
