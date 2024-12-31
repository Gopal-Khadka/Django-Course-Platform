import helpers
from django.shortcuts import render
from django.http import Http404, HttpRequest,HttpResponse

from . import services


def course_list_view(request):
    """Show list of available published courses"""
    qs = services.get_published_courses()
    template_name = "courses/list.html"
    context = {
        "queryset": qs,
        "type": qs.first().__class__.__name__.lower(),
    }
    if request.htmx:
        template_name = "courses/components/course-cards.html"
        context["queryset"] = qs[:3]
        # return HttpResponse("Courses")
    return render(request, template_name, context)


def course_detail_view(request, course_id=None, *args, **kwargs):
    """Show the detailed view of individual course"""
    course_obj = services.get_course_detail(course_id=course_id)
    if course_obj is None:
        raise Http404
    lessons_qs = services.get_course_lessons(course_obj)
    return render(
        request,
        "courses/detail.html",
        {
            "object": course_obj,
            "queryset": lessons_qs,
            "type": lessons_qs.first().__class__.__name__.lower(),
        },
    )


def lesson_detail_view(
    request: HttpRequest, course_id=None, lesson_id=None, *args, **kwargs
):
    """
    Show the detailed view of specific published course.
    Use cloudinary embedded video player to play the video.
    """
    lesson_obj = services.get_lesson_detail(course_id=course_id, lesson_id=lesson_id)
    if lesson_obj is None or course_id is None:
        raise Http404

    # show email-required page for lesson(email-required) to visitors without email
    email_id_exists = request.session.get("email_id")
    if lesson_obj.requires_email and not email_id_exists:
        return render(request, "courses/email-required.html")

    # template_name = "courses/purchase-required.html"
    context = {"object": lesson_obj}
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
