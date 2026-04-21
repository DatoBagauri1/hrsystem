from django import forms

from accounts.forms import apply_form_control
from accounts.models import get_or_create_profile

from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["full_name", "email", "phone", "cover_letter", "cv_file", "portfolio_link", "linkedin_link"]
        widgets = {"cover_letter": forms.Textarea(attrs={"rows": 6})}

    def __init__(self, *args, user=None, job=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.job = job
        for field in self.fields.values():
            apply_form_control(field)
        if user:
            profile = get_or_create_profile(user)
            self.fields["full_name"].initial = profile.full_name or user.username
            self.fields["email"].initial = user.email
            self.fields["phone"].initial = profile.phone

    def clean_cv_file(self):
        cv_file = self.cleaned_data.get("cv_file")
        if cv_file and cv_file.size > 5 * 1024 * 1024:
            raise forms.ValidationError("CV files must be 5MB or smaller.")
        return cv_file

    def clean(self):
        cleaned_data = super().clean()
        if self.user and self.job and Application.objects.filter(job=self.job, applicant=self.user).exists():
            raise forms.ValidationError("You have already applied to this vacancy.")
        return cleaned_data


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            apply_form_control(field)
