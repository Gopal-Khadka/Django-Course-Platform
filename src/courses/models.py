from django.db import models


class PublishStatus(models.TextChoices):
    PUBLISHED = "pub", "Published"
    COMING_SOON = "soon", "Coming Soon"
    DRAFT = "draft", "Draft"


class AccessRequirement(models.TextChoices):
    ANYONE = "any", "Anyone"
    EMAIL_REQUIRED = "email_required", "Email Required"


class Course(models.Model):
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(null=True, blank=True)
    # thumbnail = models.ImageField()
    access = models.CharField(
        max_length=20,
        choices=AccessRequirement.choices,
        default=AccessRequirement.EMAIL_REQUIRED,
    )
    status = models.CharField(
        max_length=15, choices=PublishStatus.choices, default=PublishStatus.DRAFT
    )

    @property
    def is_published(self):
        return self.status
