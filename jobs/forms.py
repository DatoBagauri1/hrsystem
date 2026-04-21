from django import forms

from accounts.forms import apply_form_control
from accounts.models import get_or_create_profile

from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["title", "company_name", "location", "job_type", "category", "salary_min", "salary_max", "currency", "description", "requirements", "responsibilities", "benefits", "experience_level", "application_deadline", "is_active"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 6}),
            "requirements": forms.Textarea(attrs={"rows": 5}),
            "responsibilities": forms.Textarea(attrs={"rows": 5}),
            "benefits": forms.Textarea(attrs={"rows": 4}),
            "application_deadline": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        for field in self.fields.values():
            apply_form_control(field)
        self.fields["is_active"].widget.attrs["class"] = "form-check-input"
        if user and not self.instance.pk:
            profile = get_or_create_profile(user)
            self.fields["company_name"].initial = profile.company_name
            self.fields["location"].initial = profile.location
