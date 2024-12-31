from typing import Literal
from emails.models import Email
from courses.models import Course, Lesson


def is_object_in_field(user_profile, object, field_name) -> bool:
    """Helper function to check if an object is in a specific field (favorites/cart)."""
    return getattr(user_profile, field_name).filter(id=object.id).exists()


def toggle_object_in_field(user_profile, object, field_name) -> bool:
    """Helper function to toggle an object in a specific field (favorites/cart)."""
    field = getattr(user_profile, field_name)
    if field.filter(id=object.id).exists():
        field.remove(object)
        return False  # Object was removed (unliked or removed from cart)
    else:
        field.add(object)
        return True  # Object was added (liked or added to cart)


def is_course_in_cart(email_id, public_id):
    """Check if the course in the cart of the user"""
    user_profile = Email.objects.get(id=email_id)
    course_obj = Course.objects.get(public_id=public_id)
    return is_object_in_field(user_profile, course_obj, "cart_items")


def add_to_cart(email_id, public_id):
    """Add course object to the cart of the user."""
    user_profile = Email.objects.get(id=email_id)
    course_obj = Course.objects.get(public_id=public_id)
    return toggle_object_in_field(user_profile, course_obj, "cart_items")


def is_course_liked(email_id, public_id):
    """Check if the course is liked by the user"""
    user_profile = Email.objects.get(id=email_id)
    course_obj = Course.objects.get(public_id=public_id)
    return is_object_in_field(user_profile, course_obj, "favorites")


def is_lesson_liked(email_id, public_id):
    """Check if the lesson is liked by the user"""
    user_profile = Email.objects.get(id=email_id)
    lesson_obj = Lesson.objects.get(public_id=public_id)
    return is_object_in_field(user_profile, lesson_obj, "lesson_favorites")


def toggle_favorite(email_id, public_id, model_type: Literal["lesson", "course"]):
    """A common function to toggle favorites for Course or Lesson.
    - `model_type`: can be either 'course' or 'lesson'
    """
    # Get the user profile
    user_profile = Email.objects.get(id=email_id)

    # Determine the object (Course or Lesson) and corresponding favorites field
    if model_type == "course":
        object = Course.objects.get(public_id=public_id)
        favorites_field = "favorites"
    elif model_type == "lesson":
        object = Lesson.objects.get(public_id=public_id)
        favorites_field = "lesson_favorites"
    else:
        raise ValueError("Invalid model_type. Must be either 'course' or 'lesson'.")

    # Toggle the favorite using the helper function
    return toggle_object_in_field(user_profile, object, favorites_field)


def like_course(email_id, public_id):
    """Toggle the favorite state for the course instance"""
    return toggle_favorite(email_id, public_id, model_type="course")


def like_lesson(email_id, public_id):
    """Toggle the favorite state for the lesson instance"""
    return toggle_favorite(email_id, public_id, model_type="lesson")
