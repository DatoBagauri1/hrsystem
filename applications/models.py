from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse

from accounts.models import Profile, get_or_create_profile
from jobs.models import Job


class Application(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        REVIEWED = "reviewed", "Reviewed"
        SHORTLISTED = "shortlisted", "Shortlisted"
        REJECTED = "rejected", "Rejected"
        ACCEPTED = "accepted", "Accepted"

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    cover_letter = models.TextField()
    cv_file = models.FileField(upload_to="applications/cvs/", blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=["pdf", "doc", "docx"])])
    portfolio_link = models.URLField(blank=True)
    linkedin_link = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [models.UniqueConstraint(fields=["job", "applicant"], name="unique_application_per_job")]

    def __str__(self):
        return f"{self.full_name} -> {self.job.title}"

    def get_absolute_url(self):
        return reverse("applications:application-detail", args=[self.pk])

    @property
    def status_badge_class(self):
        return {"pending": "badge-soft-warning", "reviewed": "badge-soft-info", "shortlisted": "badge-soft-primary", "rejected": "badge-soft-danger", "accepted": "badge-soft-success"}.get(self.status, "badge-soft-secondary")

    @property
    def effective_cv(self):
        if self.cv_file:
            return self.cv_file
        if self.applicant_id:
            profile = get_or_create_profile(self.applicant)
            if profile.resume:
                return profile.resume
        return None

    def clean(self):
        errors = {}
        if self.applicant_id and get_or_create_profile(self.applicant).role != Profile.Roles.SEEKER:
            errors["applicant"] = "Only job seekers can submit applications."
        if self.job_id and self.applicant_id and self.job.employer_id == self.applicant_id:
            errors["job"] = "You cannot apply to your own vacancy."
        if errors:
            raise ValidationError(errors)
