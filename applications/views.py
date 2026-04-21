from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.decorators import employer_required, seeker_required
from accounts.models import get_or_create_profile
from jobs.models import Job

from .forms import ApplicationForm, ApplicationStatusForm
from .models import Application


@seeker_required
def apply_to_job(request, slug):
    job = get_object_or_404(Job, slug=slug, is_active=True)
    if job.employer == request.user:
        messages.error(request, "You cannot apply to your own vacancy.")
        return redirect(job.get_absolute_url())
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.info(request, "You have already applied to this vacancy.")
        return redirect(job.get_absolute_url())
    form = ApplicationForm(request.POST or None, request.FILES or None, user=request.user, job=job)
    if request.method == "POST" and form.is_valid():
        application = form.save(commit=False)
        application.job = job
        application.applicant = request.user
        application.save()
        messages.success(request, "Application submitted successfully.")
        return redirect("applications:my-applications")
    return render(request, "applications/apply.html", {"form": form, "job": job})


@seeker_required
def my_applications(request):
    applications = Application.objects.filter(applicant=request.user).select_related("job").order_by("-created_at")
    page_obj = Paginator(applications, 10).get_page(request.GET.get("page"))
    return render(request, "applications/application_list.html", {"page_obj": page_obj, "applications": page_obj.object_list, "current_section": "applications"})


@login_required
def application_detail(request, pk):
    application = get_object_or_404(Application.objects.select_related("job", "job__employer__profile", "applicant__profile"), pk=pk)
    user = request.user
    profile = get_or_create_profile(user)
    if profile.is_seeker and application.applicant != user:
        messages.error(request, "You can only view your own applications.")
        return redirect("applications:my-applications")
    if profile.is_employer and application.job.employer != user:
        messages.error(request, "You can only review applicants for your own vacancies.")
        return redirect("accounts:employer-dashboard")
    status_form = ApplicationStatusForm(instance=application) if profile.is_employer else None
    return render(request, "applications/application_detail.html", {"application": application, "status_form": status_form})


@require_POST
@employer_required
def update_application_status(request, pk):
    application = get_object_or_404(Application, pk=pk, job__employer=request.user)
    form = ApplicationStatusForm(request.POST, instance=application)
    if form.is_valid():
        form.save()
        messages.success(request, "Application status updated.")
    else:
        messages.error(request, "Please choose a valid application status.")
    return redirect("applications:application-detail", pk=pk)
