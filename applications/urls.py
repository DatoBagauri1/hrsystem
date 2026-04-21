from django.urls import path

from . import views

app_name = "applications"

urlpatterns = [
    path("jobs/<slug:slug>/apply/", views.apply_to_job, name="apply"),
    path("applications/", views.my_applications, name="my-applications"),
    path("applications/<int:pk>/", views.application_detail, name="application-detail"),
    path("applications/<int:pk>/status/", views.update_application_status, name="application-status-update"),
]
