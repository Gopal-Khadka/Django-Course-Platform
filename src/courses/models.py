from django.db import models
import helpers
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


class Course(models.Model):
	title = models.CharField(max_length=200, blank=True)
	description = models.TextField(null=True, blank=True)
	thumbnail = CloudinaryField("thumbnail",null=True)
	access = models.CharField(
		max_length=20,
		choices=AccessRequirement.choices,
		default=AccessRequirement.EMAIL_REQUIRED,
	)
	status = models.CharField(
		max_length=15, choices=PublishStatus.choices, default=PublishStatus.DRAFT
	)

	def __str__(self):
		return self.title

	@property
	def is_published(self):
		return self.status
