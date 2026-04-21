from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    class Roles(models.TextChoices):
        EMPLOYER = "employer", "Employer"
        SEEKER = "seeker", "Job Seeker"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.SEEKER)

    company_name = models.CharField(max_length=255, blank=True)
    company_logo = models.ImageField(upload_to="profiles/company_logos/", blank=True, null=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    company_description = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)

    full_name = models.CharField(max_length=255, blank=True)
    profile_photo = models.ImageField(upload_to="profiles/profile_photos/", blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True, help_text="Separate skills with commas for easier scanning.")
    experience_summary = models.TextField(blank=True)
    resume = models.FileField(upload_to="profiles/resumes/", blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=["pdf", "doc", "docx"])])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user__username"]

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    @property
    def is_employer(self):
        return self.role == self.Roles.EMPLOYER

    @property
    def is_seeker(self):
        return self.role == self.Roles.SEEKER

    @property
    def display_name(self):
        if self.is_employer:
            return self.company_name or self.user.username
        return self.full_name or self.user.username

    def get_public_url(self):
        if self.is_employer:
            return reverse("accounts:employer-public-profile", args=[self.user.username])
        return "#"


def get_or_create_profile(user):
    profile, created = Profile.objects.get_or_create(
        user=user,
        defaults={
            "full_name": user.get_full_name(),
            "contact_email": user.email,
        },
    )
    if not created:
        needs_save = False
        full_name = user.get_full_name()
        if user.email and not profile.contact_email:
            profile.contact_email = user.email
            needs_save = True
        if full_name and not profile.full_name:
            profile.full_name = full_name
            needs_save = True
        if needs_save:
            profile.save()
    return profile
