from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import employer_required
from applications.models import Application

from .forms import JobForm
from .models import Job


def job_list(request):
    jobs = Job.objects.filter(is_active=True).select_related("employer__profile")
    keyword = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    job_type = request.GET.get("job_type", "").strip()
    experience = request.GET.get("experience_level", "").strip()
    salary_sort = request.GET.get("salary_sort", "").strip()
    if keyword:
        jobs = jobs.filter(Q(title__icontains=keyword) | Q(company_name__icontains=keyword) | Q(location__icontains=keyword))
    if category:
        jobs = jobs.filter(category=category)
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if experience:
        jobs = jobs.filter(experience_level=experience)
    if salary_sort == "salary_asc":
        jobs = jobs.order_by("salary_min", "-created_at")
    elif salary_sort == "salary_desc":
        jobs = jobs.order_by("-salary_max", "-created_at")
    else:
        jobs = jobs.order_by("-created_at")
    page_obj = Paginator(jobs, 9).get_page(request.GET.get("page"))
    return render(request, "jobs/job_list.html", {"page_obj": page_obj, "jobs": page_obj.object_list, "categories": Job.Category.choices, "job_types": Job.JobType.choices, "experience_levels": Job.ExperienceLevel.choices, "selected": {"q": keyword, "category": category, "job_type": job_type, "experience_level": experience, "salary_sort": salary_sort}})


def job_detail(request, slug):
    job = get_object_or_404(Job.objects.select_related("employer__profile"), slug=slug)
    if not job.is_active and (not request.user.is_authenticated or request.user != job.employer):
        messages.error(request, "That vacancy is no longer publicly available.")
        return redirect("jobs:job-list")
    has_applied = request.user.is_authenticated and request.user.profile.is_seeker and Application.objects.filter(job=job, applicant=request.user).exists()
    return render(request, "jobs/job_detail.html", {"job": job, "has_applied": has_applied})


@employer_required
def job_create(request):
    form = JobForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        job = form.save(commit=False)
        job.employer = request.user
        job.save()
        messages.success(request, "Job vacancy created successfully.")
        return redirect(job.get_absolute_url())
    return render(request, "jobs/job_form.html", {"form": form, "page_title": "Create Vacancy"})


@employer_required
def job_update(request, slug):
    job = get_object_or_404(Job, slug=slug, employer=request.user)
    form = JobForm(request.POST or None, instance=job, user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Vacancy updated successfully.")
        return redirect(job.get_absolute_url())
    return render(request, "jobs/job_form.html", {"form": form, "job": job, "page_title": "Edit Vacancy"})


@employer_required
def job_delete(request, slug):
    job = get_object_or_404(Job, slug=slug, employer=request.user)
    if request.method == "POST":
        job.delete()
        messages.success(request, "Vacancy deleted successfully.")
        return redirect("jobs:my-jobs")
    return render(request, "jobs/job_confirm_delete.html", {"job": job})


@employer_required
def employer_job_list(request):
    jobs = Job.objects.filter(employer=request.user).annotate(applicant_count=Count("applications")).order_by("-created_at")
    page_obj = Paginator(jobs, 10).get_page(request.GET.get("page"))
    return render(request, "jobs/employer_job_list.html", {"page_obj": page_obj, "jobs": page_obj.object_list, "current_section": "jobs"})


@employer_required
def applicants_list(request, slug):
    job = get_object_or_404(Job, slug=slug, employer=request.user)
    applications = Application.objects.filter(job=job).select_related("applicant__profile").order_by("-created_at")
    page_obj = Paginator(applications, 10).get_page(request.GET.get("page"))
    return render(request, "jobs/applicants_list.html", {"job": job, "page_obj": page_obj, "applications": page_obj.object_list})
