from django.contrib import admin
from .models import Email, EmailVerificationEvent,UserProfile


admin.site.register(Email)
admin.site.register(UserProfile)

@admin.register(EmailVerificationEvent)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display=["email","token"]
    readonly_fields = ["token"]
