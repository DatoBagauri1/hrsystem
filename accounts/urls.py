from django.urls import path

from .views import RoleBasedLoginView, dashboard_redirect, employer_dashboard, employer_public_profile, logout_view, profile_edit, register, seeker_dashboard

app_name = "accounts"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", RoleBasedLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/edit/", profile_edit, name="profile-edit"),
    path("dashboard/", dashboard_redirect, name="dashboard-redirect"),
    path("dashboard/employer/", employer_dashboard, name="employer-dashboard"),
    path("dashboard/seeker/", seeker_dashboard, name="seeker-dashboard"),
    path("employers/<str:username>/", employer_public_profile, name="employer-public-profile"),
]
