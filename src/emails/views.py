from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect, render
from django.http import HttpRequest
from django_htmx.http import HttpResponseClientRedirect

from . import services
from .forms import EmailForm

EMAIL_ADDRESS = settings.EMAIL_ADDRESS


def email_token_login_view(request):
    # If request is sent by htmx, then returns the login form
    if not request.htmx:
        return redirect("/")
    email_id_in_session = request.session.get("email_id")
    form = EmailForm(request.POST or None)
    template_name = "emails/hx/email_form.html"
    context = {
        "form": form,
        "message": "",
        "show_form": not email_id_in_session
    }
    if form.is_valid():
        email_val = form.cleaned_data.get("email")
        obj = services.start_verification_event(email_val)
        context["form"] = EmailForm()
        context["message"] = (
            f"Success. Check the verification mail from {EMAIL_ADDRESS} in your inbox."
        )
        # If form is valid, redirects to welcome page
        return HttpResponseClientRedirect("/welcome")
    else:
        print(form.errors)

    return render(request, template_name, context)


def verify_email_token_view(request: HttpRequest, token, *args, **kwargs):
    did_verify, msg, email_obj = services.verify_token(token)
    if not did_verify:
        try:
            del request.session["email_id"]
        except:
            pass
        messages.error(request, msg)
        # return HttpResponse(msg)
        return redirect("/login")
    messages.success(request, msg)
    request.session["email_id"] = str(email_obj.id)
    next_url = request.session.get("next_url") or "/"
    if not next_url.startswith("/"):
        next_url = "/"

    return redirect(next_url)
