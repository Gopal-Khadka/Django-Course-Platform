from emails.models import Email, UserProfile
from courses.models import Course, Lesson


def toggle_favorite(email_id, public_id, model_type):
    """
    A common function to toggle favorites for Course or Lesson.
    - `model_type`: can be either 'course' or 'lesson'
    """
    object_unliked = False

    # Get the user and user profile
    user_email = Email.objects.get(id=email_id)
    user_profile, created = UserProfile.objects.get_or_create(user=user_email)

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
