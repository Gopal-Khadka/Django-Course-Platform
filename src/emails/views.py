from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect, render,HttpResponse
from django.http import HttpRequest
from django_htmx.http import HttpResponseClientRedirect

from .models import UserProfile,Email
from courses.models import Course

from . import services
from .forms import EmailForm

EMAIL_ADDRESS = settings.EMAIL_ADDRESS


def like_course_hx_view(request: HttpRequest, course):
    if not request.htmx:
        return HttpResponse("Not a htmx request")
    user_email_id = request.session.get("email_id", None)
    if user_email_id:
        user_email = Email.objects.get(id=user_email_id)
        user_profile, created = UserProfile.objects.get_or_create(user=user_email)
        course_obj = Course.objects.get(public_id=course)
        if user_profile.favorites.filter(id = course_obj.id).exists():
            user_profile.favorites.remove(course_obj)
            return HttpResponse("Removed")
        else:
            user_profile.favorites.add(course_obj)

    return HttpResponse("Added")

def like_lesson_hx_view(request: HttpRequest, course):
    if not request.htmx:
        return HttpResponse("Not a htmx request")
    user_email_id = request.session.get("email_id", None)
    if user_email_id:
        user_email = Email.objects.get(id=user_email_id)
        user_profile, created = UserProfile.objects.get_or_create(user=user_email)
        course_obj = Course.objects.get(public_id=course)
        if user_profile.favorites.filter(id = course_obj.id).exists():
            user_profile.favorites.remove(course_obj)
            return HttpResponse("Removed")
        else:
            user_profile.favorites.add(course_obj)

    return HttpResponse("Added")




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
        obj = services.start_verification_event(email_val)
        context["form"] = EmailForm()
        context["message"] = (
            f"Success. Check the verification mail from {EMAIL_ADDRESS} in your inbox."
        )
        # If form is valid, redirects to welcome page
        # return HttpResponseClientRedirect("/welcome")
    else:
        print(form.errors)

    return render(request, template_name, context)


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
