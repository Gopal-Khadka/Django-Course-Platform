from .models import Course, PublishStatus, Lesson


def get_published_courses():
    return Course.objects.filter(status=PublishStatus.PUBLISHED)


def get_course_detail(course_id=None):
    if course_id is None:
        return None
    obj = None
    try:
        obj = Course.objects.get(id=course_id, status=PublishStatus.PUBLISHED)
    except:
        pass
    return obj


def get_lesson_detail(course_id=None, lesson_id=None):
    if lesson_id is None:
        return None
    obj = None
    try:
        obj = Lesson.objects.get(
            course___status=PublishStatus.PUBLISHED,
            course___id=course_id,
            id=lesson_id,
            status=PublishStatus.PUBLISHED,
        )
    except:
        pass
    return obj
