from django.urls import path, include
from .views import (
    email_token_login_view,
    logout_btn_hx_view,
    like_course_hx_view,
    like_lesson_hx_view,
    like_icon_hx_view,
    add_to_cart_hx_view,
    is_added_to_cart_hx_view,
    show_msg_toasts
)

app_name = "hx"
urlpatterns = [
    path("login/", email_token_login_view, name="login_form"),
    path("logout/", logout_btn_hx_view, name="logout_btn"),
    path("show-toasts/", show_msg_toasts, name="show_toasts"),
    path("like/c/<slug:course>", like_course_hx_view, name="like_course"),
    path("like/l/<slug:lesson>", like_lesson_hx_view, name="like_lesson"),
    path("add-to-cart/<course>", add_to_cart_hx_view, name="add_to_cart"),
    path(
        "is-added-to-cart/<course>", is_added_to_cart_hx_view, name="is_added_to_cart"
    ),
    path("like-icon/<instance>/<public_id>", like_icon_hx_view, name="get_like_icon"),
]
