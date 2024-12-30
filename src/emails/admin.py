from django.contrib import admin
from .models import Email, EmailVerificationEvent,UserProfile


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    search_fields=["email"]
    ordering=["-timestamp"]
    list_filter=["active"]
    list_display=["email","active"]

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    filter_horizontal=["cart_items","favorites"]

@admin.register(EmailVerificationEvent)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display=["email","token"]
    readonly_fields = ["token"]
    ordering=["-timestamp"]
