from cloudinary import CloudinaryImage
from django.contrib import admin
from django.utils.html import format_html
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "access"]
    list_filter = ["status", "access"]
    fields = ["title", "description", "thumbnail", "status", "access", "display_image"]
    readonly_fields = ["display_image"]

    def display_image(self, instance, *args, **kwargs):
        url = instance.admin_image_url
        return format_html(f"<img src='{url}'/>")

    display_image.short_description = "Current Image"
