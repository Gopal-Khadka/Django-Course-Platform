from django.db.models import QuerySet
from .models import Course, PublishStatus, Lesson


def get_published_courses():
    return Course.objects.filter(status=PublishStatus.PUBLISHED)


def get_course_detail(course_id=None):
    if course_id is None:
        return None
    obj = None
    try:
        obj = Course.objects.get(public_id=course_id, status=PublishStatus.PUBLISHED)
    except:
        pass
    return obj


def get_course_lessons(course_obj: Course = None):
    lessons = Lesson.objects.none()
    if not isinstance(course_obj, Course):
        return lessons
    lessons:QuerySet[Lesson] = course_obj.lesson_set.all()
    return lessons


def get_lesson_detail(course_id=None, lesson_id=None):
    if lesson_id is None:
        return None
    obj = None
    try:
        obj = Lesson.objects.get(
            course__public_id=course_id,
            course__status=PublishStatus.PUBLISHED,
            public_id=lesson_id,
            status__in=[PublishStatus.PUBLISHED, PublishStatus.COMING_SOON],
        )
    except:
        pass
    return obj
