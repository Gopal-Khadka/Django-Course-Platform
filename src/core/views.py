from django.conf import settings
from django.shortcuts import render

from emails.models import Email, EmailVerificationEvent
from emails.forms import EmailForm

EMAIL_ADDRESS = settings.EMAIL_ADDRESS


def home(request, *args, **kwargs):
    form = EmailForm(request.POST or None)
    context = {
        "form": form,
        "message": "",
    }
    if form.is_valid():
        email_val = form.cleaned_data.get("email")
        email_obj, created = Email.objects.get_or_create(email=email_val)
        obj = EmailVerificationEvent.objects.create(
            parent=email_obj,
            email=email_val,
        )

        
        context["form"] = EmailForm()
        context["message"] = (
            f"Success. Check the verification mail from {EMAIL_ADDRESS} in your inbox."
        )
    else:
        print(form.errors)

    return render(request, "home.html", context)
