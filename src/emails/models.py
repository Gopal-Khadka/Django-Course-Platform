from django.db import models


class Email(models.Model):
    email = models.EmailField(
        unique=True,
        blank=False,
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class EmailVerificationEvent(models.Model):
    parent = models.ForeignKey(Email, on_delete=models.SET_NULL, null=True)
    email = models.EmailField()
    # ip_address
    # token
    expired = models.BooleanField(db_default=False)
    attempts = models.IntegerField(default=0)
    last_attempt_at = models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True
    )
    expired_at = models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)
