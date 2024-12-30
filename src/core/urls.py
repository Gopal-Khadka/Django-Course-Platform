from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from emails.views import (
    verify_email_token_view,
    email_token_login_view,
    logout_btn_hx_view,
    like_course_hx_view,like_lesson_hx_view
)
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("contact", views.contact, name="contact"),
    path("login/", views.login_logout_view, name="login"),
    path("logout/", views.login_logout_view, name="logout"),
    path("hx/login/", email_token_login_view, name="login_form"),
    path("hx/logout/", logout_btn_hx_view, name="logout_btn"),
    path("hx/like/c/<slug:course>", like_course_hx_view, name="like_course"),
    path("hx/like/l/<slug:lesson>", like_lesson_hx_view, name="like_lesson"),
    path(
        "verify/<uuid:token>", verify_email_token_view, name="verify_email_token_view"
    ),
    path("admin/", admin.site.urls),
    path("courses/", include("courses.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # for django-tailwind-browser reload
    urlpatterns += [path("__reload__/", include("django_browser_reload.urls"))]
