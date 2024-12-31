from django.conf import settings
from django.shortcuts import render

from emails import services
from emails.forms import EmailForm

EMAIL_ADDRESS = settings.EMAIL_ADDRESS


def home(request, *args, **kwargs):
    """
    Show home page to the user.
    Asks for login to new users.
    Shows logout option to loggedin user.
    """
    template_name = "home.html"
    print(request.session.get("email_id","None"))
    return render(request, template_name)

def contact(request, *args, **kwargs):
    template_name = "base/contact.html"
    return render(request, template_name)


def login_logout_view(request):

    return render(request, "auth/login-logout.html")
