from django.contrib import admin

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "job", "applicant", "status", "created_at")
    list_filter = ("status", "created_at", "job__job_type")
    search_fields = ("full_name", "email", "job__title", "job__company_name", "applicant__username")
    ordering = ("-created_at",)
