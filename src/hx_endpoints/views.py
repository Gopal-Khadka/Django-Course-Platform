from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django_htmx.http import HttpResponseClientRedirect

from emails import services as email_services
from . import services
from emails.forms import EmailForm


EMAIL_ADDRESS = settings.EMAIL_ADDRESS


def like_icon_hx_view(request: HttpRequest, instance, public_id):
    if not request.htmx:
        return HttpResponse("Not a htmx request.")
    instance_already_liked = False
    email_id = request.session.get("email_id")
    if instance == "course":
        instance_already_liked = services.is_course_liked(email_id, public_id)
    else:
        instance_already_liked = services.is_lesson_liked(email_id, public_id)
    if instance_already_liked:
        return render(request, "hx_endpoints/components/filled-like.html")
    return render(request, "hx_endpoints/components/hollow-like.html")


def like_course_hx_view(request: HttpRequest, course):
    if not request.htmx:
        return HttpResponse("Not a htmx request")
    user_email_id = request.session.get("email_id", None)
    if user_email_id:
        course_unliked = services.like_course(user_email_id, course)
        if course_unliked:
            return render(request, "hx_endpoints/components/hollow-like.html")
        return render(request, "hx_endpoints/components/filled-like.html")


def like_lesson_hx_view(request: HttpRequest, lesson):
    if not request.htmx:
        return HttpResponse("Not a htmx request")
    user_email_id = request.session.get("email_id", None)
    if user_email_id:
        lesson_unliked = services.like_lesson(user_email_id, lesson)
        if lesson_unliked:
            return render(request, "hx_endpoints/components/hollow-like.html")
        return render(request, "hx_endpoints/components/filled-like.html")


def logout_btn_hx_view(request: HttpRequest):
    """
    If GET: Returns logout button
    If POST: Logs out the user by deleting session['email_id'] and redirects to login page
    """
    if not request.htmx:
        return redirect("/")
    if request.method == "POST":
        try:
            del request.session["email_id"]  # remove email-id from session i.e. logout
        except:
            pass
        email_id_in_session = request.session.get("email_id")
        if not email_id_in_session:  # if logged out, redirect to home (login form)
            return HttpResponseClientRedirect("/")

    return render(
        request, "emails/hx/logout-btn.html"
    )  # return for GET and logged in state


def email_token_login_view(request):
    """Renders the login form and triggers the email verification event"""
    # If request is sent by htmx, then returns the login form
    if not request.htmx:
        return redirect("/")
    email_id_in_session = request.session.get("email_id")
    form = EmailForm(request.POST or None)
    template_name = "emails/hx/email-form.html"
    context = {"form": form, "message": "", "show_form": not email_id_in_session}
    if form.is_valid():
        email_val = form.cleaned_data.get("email")
        obj = email_services.start_verification_event(email_val)
        context["form"] = EmailForm()
        context["message"] = (
            f"Success. Check the verification mail from {EMAIL_ADDRESS} in your inbox."
        )
        # If form is valid, redirects to welcome page
        # return HttpResponseClientRedirect("/welcome")
    else:
        print(form.errors)

    return render(request, template_name, context)
