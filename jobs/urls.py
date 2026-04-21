from django.urls import path

from . import views

app_name = "jobs"

urlpatterns = [
    path("", views.job_list, name="job-list"),
    path("create/", views.job_create, name="job-create"),
    path("mine/", views.employer_job_list, name="my-jobs"),
    path("<slug:slug>/", views.job_detail, name="job-detail"),
    path("<slug:slug>/edit/", views.job_update, name="job-edit"),
    path("<slug:slug>/delete/", views.job_delete, name="job-delete"),
    path("<slug:slug>/applicants/", views.applicants_list, name="job-applicants"),
]
