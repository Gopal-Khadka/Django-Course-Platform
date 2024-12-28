from django.conf import settings
from django.core.mail import send_mail

from .models import Email, EmailVerificationEvent

EMAIL_HOST_USER = settings.EMAIL_HOST_USER


def verify_email(email):
    """Check if given email already exists with inactive status in DB"""
    qs = Email.objects.filter(email__iexact=email, active=False)
    return qs.exists()


def get_verification_email_msg(
    verification_instance: EmailVerificationEvent, as_html=False
):
    if not isinstance(verification_instance, EmailVerificationEvent):
        return None
    if as_html:
        return f"<h1>{verification_instance.id}</h1>"
    return f"{verification_instance.id}"


def start_verification_event(email):
    """Gets/creates email object with given email
    and sends the verification email to the given email"""
    email_obj, created = Email.objects.get_or_create(email=email)
    obj = EmailVerificationEvent.objects.create(
        parent=email_obj,
        email=email,
    )
    sent = send_verification_email(obj) == 1
    return sent


def send_verification_email(obj: EmailVerificationEvent):
    email = obj.email
    # send verification email
    subject = "Email verification"
    text_msg = get_verification_email_msg(obj)
    text_html = get_verification_email_msg(obj, as_html=True)
    sender_email = EMAIL_HOST_USER
    recepient_list = [email]
    # send email to verify user
    # make email sending as celery task to avoid delay
    did_send = send_mail(
        subject,
        text_msg,
        sender_email,
        recepient_list,
        fail_silently=False,
        html_message=text_html,
    )
    return did_send
