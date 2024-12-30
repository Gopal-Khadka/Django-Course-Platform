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
    if hasattr(instance, "path"):
        path = str(instance.path)
        if path.startswith("/"):
            path = path[1:]
        if path.endswith("/"):
            path = path[:-1]
        return path

    public_id = instance.public_id
    model_name = instance.__class__.__name__
    model_name_slug = slugify(model_name)
    if not public_id:
        return f"{model_name_slug}"
    return f"{model_name_slug}/{public_id}"


def get_display_name(instance, *args, **kwargs):
    title = instance.title
    if title:
        return str(title)
    model_name = instance.__class__.__name__
    return f"{model_name} Upload"


class Course(models.Model):
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(null=True, blank=True)
    public_id = models.CharField(max_length=210, blank=True, null=True, db_index=True)
    # price
    # discount
    # reviews
    thumbnail = CloudinaryField(
        "thumbnail",
        null=True,
        public_id_prefix=get_public_id_prefix,
        display_name=get_display_name,
        tags=["course", "thumbnail"],
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
    def avg_rating(self):
        reviews:CourseReviews = self.reviews
        avg_rating = int(reviews.aggregate(models.Avg('rating')).get("rating__avg",0))
        return avg_rating
    
    @property
    def reviews_count(self):
        return self.reviews.count()

    @property
    def admin_image_url(self):
        url = helpers.get_cloudinary_image_object(
            self, width=300, field_name="thumbnail"
        )
        return url

    @property
    def list_image_url(self):
        url = helpers.get_cloudinary_image_object(
            self, width=400, field_name="thumbnail"
        )
        return url

    @property
    def detail_image_url(self):
        url = helpers.get_cloudinary_image_object(
            self, width=750, field_name="thumbnail"
        )
        return url

    def get_absolute_url(self):
        return self.path

    @property
    def path(self):
        return f"/courses/{self.public_id}"

    def get_display_name(self):
        return f"{self.title} - Course"

    def get_image_thumbnail(self, width=500, as_html=False):
        return helpers.get_cloudinary_image_object(self, width=width, as_html=as_html)


class CourseReviews(models.Model):
    email = models.ForeignKey("emails.email", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.email}"

    class Meta:
        verbose_name = "Course Review"
        ordering = ['-created_at'] 


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # course_id = when foreign key is added, related id field is also automatically added.
    public_id = models.CharField(max_length=210, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(null=True, blank=True)
    thumbnail = CloudinaryField(
        "image",
        blank=True,
        null=True,
        public_id_prefix=get_public_id_prefix,
        display_name=get_display_name,
        tags=["lesson", "thumbnail"],
    )
    video = CloudinaryField(
        "video",
        blank=True,
        null=True,
        type="private",
        resource_type="video",
        public_id_prefix=get_public_id_prefix,
        display_name=get_display_name,
        tags=["lesson", "video"],
    )
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

    def get_absolute_url(self):
        return self.path

    @property
    def path(self):
        course_path = self.course.path
        if course_path.endswith("/"):
            course_path = course_path[:-1]
        return f"{course_path}/lessons/{self.public_id}"

    def get_display_name(self):
        return f"{self.title} - {self.course.get_display_name}"

    @property
    def is_coming_soon(self):
        return self.status == PublishStatus.COMING_SOON

    @property
    def has_video(self):
        return self.video is not None

    @property
    def requires_email(self):
        return self.course.access == AccessRequirement.EMAIL_REQUIRED

    @property
    def admin_image_url(self):
        url = helpers.get_cloudinary_image_object(
            self, width=300, field_name="thumbnail"
        )
        return url

    @property
    def list_image_url(self):
        url = helpers.get_cloudinary_image_object(
            self, width=400, field_name="thumbnail"
        )
        return url

    @property
    def detail_image_url(self):
        url = helpers.get_cloudinary_image_object(
            self, width=750, field_name="thumbnail"
        )
        return url
