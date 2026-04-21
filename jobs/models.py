from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone


class Job(models.Model):
    class JobType(models.TextChoices):
        FULL_TIME = "full-time", "Full-time"
        PART_TIME = "part-time", "Part-time"
        INTERNSHIP = "internship", "Internship"
        REMOTE = "remote", "Remote"
        HYBRID = "hybrid", "Hybrid"
        CONTRACT = "contract", "Contract"

    class Category(models.TextChoices):
        ENGINEERING = "engineering", "Engineering"
        DESIGN = "design", "Design"
        MARKETING = "marketing", "Marketing"
        SALES = "sales", "Sales"
        PRODUCT = "product", "Product"
        OPERATIONS = "operations", "Operations"
        FINANCE = "finance", "Finance"
        HUMAN_RESOURCES = "human-resources", "Human Resources"
        CUSTOMER_SUPPORT = "customer-support", "Customer Support"

    class ExperienceLevel(models.TextChoices):
        JUNIOR = "junior", "Junior"
        MID = "mid", "Mid"
        SENIOR = "senior", "Senior"

    class Currency(models.TextChoices):
        USD = "USD", "USD"
        EUR = "EUR", "EUR"
        GBP = "GBP", "GBP"
        GEL = "GEL", "GEL"

    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=20, choices=JobType.choices)
    category = models.CharField(max_length=30, choices=Category.choices)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.USD)
    description = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField()
    benefits = models.TextField(blank=True)
    experience_level = models.CharField(max_length=10, choices=ExperienceLevel.choices)
    is_active = models.BooleanField(default=True)
    application_deadline = models.DateField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.company_name}"

    def get_absolute_url(self):
        return reverse("jobs:job-detail", args=[self.slug])

    @property
    def application_count(self):
        return self.applications.count()

    @property
    def salary_display(self):
        if self.salary_min and self.salary_max:
            return f"{self.currency} {int(self.salary_min):,} - {int(self.salary_max):,}"
        if self.salary_min:
            return f"From {self.currency} {int(self.salary_min):,}"
        if self.salary_max:
            return f"Up to {self.currency} {int(self.salary_max):,}"
        return "Salary not disclosed"

    def clean(self):
        if self.salary_min and self.salary_max and self.salary_min > self.salary_max:
            raise ValidationError({"salary_min": "Minimum salary cannot be greater than maximum salary."})
        if self.is_active and self.application_deadline and self.application_deadline < timezone.localdate():
            raise ValidationError({"application_deadline": "Active jobs cannot have a deadline in the past."})

    def save(self, *args, **kwargs):
        base_slug = slugify(f"{self.title}-{self.company_name}")[:220] or "job"
        slug = base_slug
        counter = 1
        while Job.objects.exclude(pk=self.pk).filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        self.slug = slug
        super().save(*args, **kwargs)
