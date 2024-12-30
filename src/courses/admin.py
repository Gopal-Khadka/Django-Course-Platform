import helpers
from cloudinary import CloudinaryImage
from django.contrib import admin
from django.utils.html import format_html
from .models import Course, Lesson, CourseReviews


class LessonInline(admin.StackedInline):
    model = Lesson
    readonly_fields = ["public_id", "updated", "display_image", "display_video"]
    extra = 0

    def display_image(self, instance, *args, **kwargs):
        url = helpers.get_cloudinary_image_object(
            instance, field_name="thumbnail", width=200
        )
        return format_html(f"<img src='{url}'/>")

    display_image.short_description = "Current Image"

    def display_video(self, instance, *args, **kwargs):
        video_embed_html = helpers.get_cloudinary_video_object(
            instance,
            field_name="video",
            width=500,
            as_html=True,
            controls=True,
            autoplay=True,
        )
        return video_embed_html

    display_video.short_description = "Current VIdeo"


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ["title", "status", "access","avg_rating","reviews_count",]
    list_filter = ["status", "access"]
    search_fields=["title","status"]
    fields = [
        "public_id",
        "title",
        "description",
        "avg_rating",
        "reviews_count",
        "thumbnail",
        "status",
        "access",
        "display_image",
    ]
    readonly_fields = [
        "public_id",
        "display_image",
        "avg_rating",
        "reviews_count",
    ]

    def display_image(self, instance, *args, **kwargs):
        url = instance.admin_image_url
        return format_html(f"<img src='{url}'/>")

    display_image.short_description = "Current Image"


@admin.register(CourseReviews)
class CourseReviewAdmin(admin.ModelAdmin):
    list_display = ("email", "course", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("email__email", "course__name", "review")
