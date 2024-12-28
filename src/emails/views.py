from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse
from . import services


# Create your views here.
def verify_email_token_view(request, token, *args, **kwargs):
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
    return redirect("/")
