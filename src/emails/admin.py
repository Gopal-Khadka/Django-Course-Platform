from django.contrib import admin
from .models import Email, EmailVerificationEvent


admin.site.register(Email)

@admin.register(EmailVerificationEvent)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display=["email","token"]
    readonly_fields = ["token"]
