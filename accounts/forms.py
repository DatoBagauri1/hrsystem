from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, get_or_create_profile


def apply_form_control(field):
    base_class = "form-control"
    if isinstance(field.widget, forms.Textarea):
        field.widget.attrs["rows"] = field.widget.attrs.get("rows", 4)
    if isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
        base_class = "form-select"
    field.widget.attrs["class"] = base_class


class StyledAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}), strip=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            apply_form_control(field)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    role = forms.ChoiceField(choices=Profile.Roles.choices)
    display_name = forms.CharField(max_length=255, help_text="Company name for employers, full name for job seekers.")

    class Meta:
        model = User
        fields = ("username", "email", "role", "display_name", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            apply_form_control(field)

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            profile = get_or_create_profile(user)
            profile.role = self.cleaned_data["role"]
            if profile.is_employer:
                profile.company_name = self.cleaned_data["display_name"]
                profile.contact_email = user.email
            else:
                profile.full_name = self.cleaned_data["display_name"]
            profile.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["company_name", "company_logo", "website", "location", "company_description", "contact_email", "full_name", "profile_photo", "phone", "city", "bio", "skills", "experience_summary", "resume"]
        widgets = {
            "company_description": forms.Textarea(attrs={"rows": 5}),
            "bio": forms.Textarea(attrs={"rows": 4}),
            "skills": forms.Textarea(attrs={"rows": 3}),
            "experience_summary": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        for field in self.fields.values():
            apply_form_control(field)
        role = self.instance.role if self.instance.pk else get_or_create_profile(user).role
        if role == Profile.Roles.EMPLOYER:
            for name in ["full_name", "profile_photo", "phone", "city", "bio", "skills", "experience_summary", "resume"]:
                self.fields.pop(name, None)
            self.fields["company_name"].required = True
            self.fields["location"].required = True
            self.fields["company_description"].required = True
            self.fields["contact_email"].required = True
        else:
            for name in ["company_name", "company_logo", "website", "location", "company_description", "contact_email"]:
                self.fields.pop(name, None)
            self.fields["full_name"].required = True
            self.fields["phone"].required = True
            self.fields["city"].required = True

    def clean_resume(self):
        resume = self.cleaned_data.get("resume")
        if resume and resume.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Resume files must be 5MB or smaller.")
        return resume
