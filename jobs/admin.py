from django.contrib import admin

from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "company_name",
        "employer",
        "job_type",
        "experience_level",
        "is_active",
        "application_deadline",
        "created_at",
    )
    list_filter = ("job_type", "experience_level", "is_active", "currency", "created_at")
    search_fields = ("title", "company_name", "location", "category", "employer__username")
    prepopulated_fields = {"slug": ("title", "company_name")}
    ordering = ("-created_at",)
