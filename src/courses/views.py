from django.shortcuts import render
from django.http import Http404, JsonResponse

from . import services


def course_list_view(request):
    qs = services.get_published_courses()
    print(qs)
    return JsonResponse({"data": [x.id for x in qs]})
    return render(request, "courses/list.html", {})


def course_detail_view(request, course_id=None, *args, **kwargs):
    course_obj = services.get_course_detail(course_id=course_id)
    if course_obj is None:
        raise Http404
    lessons_qs = course_obj.lesson_set.all()
    print(lessons_qs)
    return JsonResponse({"data": course_obj.id})
    return render(request, "courses/detail.html", {})


def lesson_detail_view(request, course_id=None, lesson_id=None, *args, **kwargs):
    lesson_obj = services.get_lesson_detail(course_id=course_id, lesson_id=lesson_id)
    if lesson_obj is None:
        raise Http404
    return JsonResponse({"data": lesson_obj.id})
    return render(request, "courses/lesson.html", {})
