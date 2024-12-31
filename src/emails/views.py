from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpRequest


from . import services

def verify_email_token_view(request: HttpRequest, token, *args, **kwargs):
    """
    Verifies the provided token before the expiry and max attempts limit.
    If unverified, returns back to login page.
    If verified, adds email-id to session object.
    """
    did_verify, msg, email_obj = services.verify_token(token)
    if not did_verify:
        try:
            del request.session["email_id"]
        except:
            pass
        messages.error(request, msg)
        # return HttpResponse(msg)
        return redirect("/hx/login")
    messages.success(request, msg)
    request.session["email_id"] = str(email_obj.id)

    # Refer to "courses.views.lesson_detail_view()"
    next_url = request.session.get("next_url") or "/"
    if not next_url.startswith("/"):
        next_url = "/"

    return redirect(next_url)
