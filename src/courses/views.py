import helpers
from django.shortcuts import render
from django.http import Http404

from . import services


def course_list_view(request):
    qs = services.get_published_courses()
    print(qs)
    # return JsonResponse({"data": [x.path for x in qs]})
    return render(request, "courses/list.html", {"courses_list": qs})


def course_detail_view(request, course_id=None, *args, **kwargs):
    course_obj = services.get_course_detail(course_id=course_id)
    if course_obj is None:
        raise Http404
    lessons_qs = services.get_course_lessons(course_obj)
    # return JsonResponse({"data": course_obj.id, "lessons": [x.path for x in lessons_qs]})
    return render(
        request,
        "courses/detail.html",
        {
            "object": course_obj,
            "lessons_list": lessons_qs,
        },
    )


def lesson_detail_view(request, course_id=None, lesson_id=None, *args, **kwargs):
    lesson_obj = services.get_lesson_detail(course_id=course_id, lesson_id=lesson_id)
    if lesson_obj is None or course_id is None:
        raise Http404
    # template_name = "courses/purchase-required.html"
    context = {"lesson_obj": lesson_obj}
    template_name = "courses/lesson-coming-soon.html"
    if not lesson_obj.is_coming_soon and lesson_obj.has_video:
        # Lesson is already published and Video is available for the lesson
        template_name = "courses/lesson.html"
        video_embed_html = helpers.get_cloudinary_video_object(
            lesson_obj,
            field_name="video",
            width=600,
            as_html=True,
            autoplay=True,
            quality="auto:best",
        )
        context["video_embed"] = video_embed_html

    return render(request, template_name, context)
