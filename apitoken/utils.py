# utils.py

from django.core.mail import send_mail
from django.conf import settings

def send_email(subject, message, recipient_list):
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,  # Sender's email
            recipient_list,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False
