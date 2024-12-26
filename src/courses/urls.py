from django.urls import path

from . import views

urlpatterns = [
    path("", views.course_list_view, name="course_list_view"),
    path("<int:course_id>/", views.course_detail_view, name="course_detail_view"),
    path(
        "<int:course_id>/lesson/<int:lesson_id>/",
        views.lesson_detail_view,
        name="lesson_detail_view",
    ),
]
