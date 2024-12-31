from emails.models import Email
from courses.models import Course, Lesson

def is_course_in_cart(email_id, public_id):
    user_profile = Email.objects.get(id=email_id)
    course_obj = Course.objects.get(public_id=public_id)
    return user_profile.cart_items.contains(course_obj)

def add_to_cart(email_id, public_id):
    user_profile = Email.objects.get(id=email_id)
    course_obj = Course.objects.get(public_id=public_id)
    if user_profile.cart_items.contains(course_obj):
        user_profile.cart_items.remove(course_obj)
        return False
    else:
        user_profile.cart_items.add(course_obj)
    return True


def is_course_liked(email_id, public_id):
    user_profile = Email.objects.get(id=email_id)
    course_obj = Course.objects.get(public_id=public_id)
    return user_profile.favorites.contains(course_obj)

def is_lesson_liked(email_id, public_id):
    user_profile = Email.objects.get(id=email_id)
    lesson_obj = Lesson.objects.get(public_id=public_id)
    return user_profile.lesson_favorites.contains(lesson_obj)


def toggle_favorite(email_id, public_id, model_type):
    """
    A common function to toggle favorites for Course or Lesson.
    - `model_type`: can be either 'course' or 'lesson'
    """
    object_unliked = False

    # Get the user and user profile
    user_profile = Email.objects.get(id=email_id)

    # Determine the object (Course or Lesson) based on `model_type`
    if model_type == "course":
        object = Course.objects.get(public_id=public_id)
        favorites_field = "favorites"  # Target the 'favorites' field for courses
    elif model_type == "lesson":
        object = Lesson.objects.get(public_id=public_id)
        favorites_field = (
            "lesson_favorites"  # Target the 'lesson_favorites' field for lessons
        )
    else:
        raise ValueError("Invalid model_type. Must be either 'course' or 'lesson'.")

    # Toggle the favorite
    if getattr(user_profile, favorites_field).filter(id=object.id).exists():
        getattr(user_profile, favorites_field).remove(object)
        object_unliked = True
    else:
        getattr(user_profile, favorites_field).add(object)

    return object_unliked


def like_course(email_id, public_id):
    """Toggle the favorite state for the course instance"""
    return toggle_favorite(email_id, public_id, model_type="course")


def like_lesson(email_id, public_id):
    """Toggle the favorite state for the lesson instance"""
    return toggle_favorite(email_id, public_id, model_type="lesson")
