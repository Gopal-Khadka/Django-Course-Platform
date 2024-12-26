from django.shortcuts import render

from . import services

def course_list_view(request):
    qs = services.get_published_courses()
    return render(request, "courses/list.html", {})


def course_detail_view(request):
    return render(request, "courses/detail.html", {})


def lesson_detail_view(request):
    return render(request, "courses/lesson.html", {})
