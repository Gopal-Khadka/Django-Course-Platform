from django.conf import settings
from django.shortcuts import render

from emails import services
from emails.forms import EmailForm

EMAIL_ADDRESS = settings.EMAIL_ADDRESS


def home(request, *args, **kwargs):
    template_name = "home.html"

    return render(request, template_name)
