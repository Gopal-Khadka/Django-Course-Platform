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

    def display_image(self, instance,*args,**kwargs):
        url = instance.thumbnail.url
        cloudinary_id = str(instance.thumbnail)
        cloudinary_html = CloudinaryImage(cloudinary_id).image(width=500)
        return format_html(cloudinary_html)

    display_image.short_description = "Current Image"