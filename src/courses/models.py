import helpers
import uuid
from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

helpers.cloudinary_init()


class PublishStatus(models.TextChoices):
    PUBLISHED = "pub", "Published"
    COMING_SOON = "soon", "Coming Soon"
    DRAFT = "draft", "Draft"


class AccessRequirement(models.TextChoices):
    ANYONE = "any", "Anyone"
    EMAIL_REQUIRED = "email_required", "Email Required"


def handle_upload(instance, filename):
    return f"{filename}"


def generate_public_id(instance, *args, **kwargs):
    title = instance.title
    unique_id = str(uuid.uuid4())
    if not title:
        return unique_id
    slug = slugify(title)
    unique_id_short = unique_id.replace("-", "")[:5]
    return f"{slug}-{unique_id_short}"


def get_public_id_prefix(instance, *args, **kwargs):
    public_id = instance.public_id
    if not public_id:
        return "courses"
    return f"courses/{public_id}"


def get_display_name(instance, *args, **kwargs):
    title = instance.title
    if title:
        return str(title)
    return "Course Upload"


def get_course_tags(*args, **kwargs):
    return ["course", "thumbnail"]


class Course(models.Model):
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(null=True, blank=True)
    public_id = models.CharField(
        max_length=210, blank=True, null=True
    )  # slug of the title
    thumbnail = CloudinaryField(
        "thumbnail",
        null=True,
        public_id_prefix=get_public_id_prefix,
        display_name=get_display_name,
        tags=get_course_tags,
    )
    access = models.CharField(
        max_length=20,
        choices=AccessRequirement.choices,
        default=AccessRequirement.EMAIL_REQUIRED,
    )
    status = models.CharField(
        max_length=15, choices=PublishStatus.choices, default=PublishStatus.DRAFT
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.public_id is None:
            self.public_id = generate_public_id(self)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def is_published(self):
        return self.status

    @property
    def admin_image_url(self):
        url = self.get_image_thumbnail()
        return url

    def get_image_thumbnail(self, width=500, as_html=False):
        if not self.thumbnail:
            return ""
        image_options = {"width": width}
        if as_html:
            return self.thumbnail.image(**image_options)
        url = self.thumbnail.build_url(**image_options)
        return url


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # course_id = when foreign key is added, related id field is also automatically added.
    public_id = models.CharField(max_length=210, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(null=True, blank=True)
    thumbnail = CloudinaryField("image", blank=True, null=True)
    video = CloudinaryField("video", blank=True, null=True, resource_type="video")
    order = models.IntegerField(default=0)
    can_preview = models.BooleanField(
        default=False, help_text="Can user without course access see this?"
    )
    status = models.CharField(
        max_length=15, choices=PublishStatus.choices, default=PublishStatus.PUBLISHED
    )
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-updated"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.public_id is None:
            self.public_id = generate_public_id(self)
        return super().save(*args, **kwargs)
