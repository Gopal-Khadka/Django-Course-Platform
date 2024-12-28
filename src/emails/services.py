from django.conf import settings
from django.core.mail import send_mail
from uuid import UUID
from django.utils import timezone
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
    link = verification_instance.get_link()
    if as_html:
        return f"""
        <h1>Verify your email with given link:</h1> 
        <p><a href='{link}'>Verify</a></p>
        """
    return f"Verify your email with given link: \n {link}"


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


def verify_token(token: UUID, max_attempts=5) -> tuple[bool, str]:
    """Verify the url provided token with generated token in db"""
    qs = EmailVerificationEvent.objects.filter(token=token)
    if not qs.exists() and not qs.count() == 1:
        print("Invalid token")
        # for non-existent token
        return False, "Invalid Token"
    email_expired = qs.filter(expired=True)
    if email_expired.exists():
        # for expired token
        return False, "Token is already expired. Try again."

    max_attempts_reached = qs.filter(attempts__gte=max_attempts)
    if max_attempts_reached.exists():
        # for too many attempts
        # max_attempts_reached.update()
        return False, "Token expired. Used too many times."

    # for valid token
    obj = qs.first()
    obj.attempts += 1
    obj.last_attempt_at = timezone.now()
    if obj.attempts > max_attempts:
        obj.expired = True
        obj.expired_at = timezone.now()
    obj.save()
    return True, "Welcome to the site"
