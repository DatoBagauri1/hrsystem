from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from applications.models import Application
from jobs.models import Job

from .decorators import employer_required, seeker_required
from .forms import ProfileForm, RegistrationForm, StyledAuthenticationForm
from .models import Profile, get_or_create_profile


class RoleBasedLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = StyledAuthenticationForm

    def form_valid(self, form):
        messages.success(self.request, f"Welcome back, {form.get_user().username}.")
        return super().form_valid(form)

    def get_success_url(self):
        redirect_to = self.get_redirect_url()
        if redirect_to:
            return redirect_to
        profile = get_or_create_profile(self.request.user)
        return reverse("accounts:employer-dashboard") if profile.is_employer else reverse("accounts:seeker-dashboard")


def register(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard-redirect")
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created successfully. You can now sign in.")
        return redirect("accounts:login")
    return render(request, "accounts/register.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("core:home")


@login_required
def dashboard_redirect(request):
    profile = get_or_create_profile(request.user)
    return redirect("accounts:employer-dashboard") if profile.is_employer else redirect("accounts:seeker-dashboard")


@login_required
def profile_edit(request):
    profile = get_or_create_profile(request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile, user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your profile has been updated.")
        return redirect("accounts:dashboard-redirect")
    return render(request, "accounts/profile_form.html", {"form": form, "profile": profile})


@employer_required
def employer_dashboard(request):
    jobs = Job.objects.filter(employer=request.user).annotate(applicant_count=Count("applications")).order_by("-created_at")
    recent_applications = Application.objects.filter(job__employer=request.user).select_related("job", "applicant__profile").order_by("-created_at")[:6]
    stats = {
        "total_jobs": jobs.count(),
        "active_jobs": jobs.filter(is_active=True).count(),
        "total_applications": Application.objects.filter(job__employer=request.user).count(),
        "shortlisted": Application.objects.filter(job__employer=request.user, status="shortlisted").count(),
    }
    return render(request, "accounts/employer_dashboard.html", {"stats": stats, "jobs": jobs[:5], "recent_applications": recent_applications, "current_section": "dashboard"})


@seeker_required
def seeker_dashboard(request):
    applications = Application.objects.filter(applicant=request.user).select_related("job").order_by("-created_at")
    latest_jobs = Job.objects.filter(is_active=True).exclude(applications__applicant=request.user)[:6]
    stats = {
        "total_sent": applications.count(),
        "pending": applications.filter(status="pending").count(),
        "shortlisted": applications.filter(status="shortlisted").count(),
        "accepted": applications.filter(status="accepted").count(),
    }
    return render(request, "accounts/seeker_dashboard.html", {"stats": stats, "applications": applications[:5], "latest_jobs": latest_jobs, "current_section": "dashboard"})


def employer_public_profile(request, username):
    employer = get_object_or_404(
        User.objects.select_related("profile"),
        username=username,
        profile__role=Profile.Roles.EMPLOYER,
    )
    jobs = Job.objects.filter(employer=employer, is_active=True).order_by("-created_at")
    return render(request, "accounts/employer_public_profile.html", {"employer_user": employer, "jobs": jobs})
