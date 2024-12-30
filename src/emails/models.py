import uuid
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from courses.models import Course

User = get_user_model()


class Email(models.Model):
    email = models.EmailField(
        unique=True,
        blank=False,
    )
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(Email, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(Course, related_name="cart_users", blank=True)
    favorites = models.ManyToManyField(
        Course, related_name="favorite_users", blank=True
    )
    def __str__(self):
        return f"{self.user.email}'s Profile"


# model to handle relation between each course and each user
# class Purchase(models.Model):
#     email = models.ForeignKey(Email, on_delete=models.SET_NULL, null=True)
#     course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)


class EmailVerificationEvent(models.Model):
    parent = models.ForeignKey(Email, on_delete=models.SET_NULL, null=True)
    email = models.EmailField()
    # ip_address
    token = models.UUIDField(default=uuid.uuid1)
    expired = models.BooleanField(db_default=False)
    attempts = models.IntegerField(default=0)
    last_attempt_at = models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True
    )
    expired_at = models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.parent.email

    def get_link(self):
        return f"{settings.BASE_URL}/verify/{self.token}"
