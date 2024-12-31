from django.urls import path, include
from .views import (
    email_token_login_view,
    logout_btn_hx_view,
    like_course_hx_view,
    like_lesson_hx_view,
)

urlpatterns = [
    path("login/", email_token_login_view, name="login_form"),
    path("logout/", logout_btn_hx_view, name="logout_btn"),
    path("like/c/<slug:course>", like_course_hx_view, name="like_course"),
    path("like/l/<slug:lesson>", like_lesson_hx_view, name="like_lesson"),
]
