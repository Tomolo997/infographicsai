import logging

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode

import resend

logger = logging.getLogger(__name__)

def send_verification_email(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    # Use proper URL based on environment
    verification_link = f"{settings.SITE_URL}/api/account/verify/{uid}/{token}/"
    
    # Set Resend API key
    resend.api_key = settings.RESEND_API
    
    # Prepare email content
    email_subject = "Verify Your ainfographic Account"
    context = {"user": user, "verification_link": verification_link}
    html_content = render_to_string("account_verification_email.html", context)
    text_content = strip_tags(html_content)
    
    # Set up email parameters for Resend
    params = {
        "from": f"Ainfographic <{settings.DEFAULT_FROM_EMAIL}>",
        "to": [user.email],
        "subject": email_subject,
        "html": html_content,
        "text": text_content,
    }
    
    # Send email using Resend
    try:
        email_response = resend.Emails.send(params=params)
        logger.info(f"✅ Verification email sent to {user.email}")
        logger.info(f"🔗 Verification link: {verification_link}")
        return email_response
    except Exception as e:
        logger.error(f"❌ Error sending verification email: {e}")
        return None
