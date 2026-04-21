from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "display_name", "location", "contact_email", "updated_at")
    list_filter = ("role", "updated_at")
    search_fields = ("user__username", "user__email", "company_name", "full_name", "location")
    ordering = ("user__username",)
