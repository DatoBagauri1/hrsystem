from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from .models import Profile, get_or_create_profile


def _role_redirect(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard-redirect")
    return redirect("accounts:login")


def employer_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please sign in to access that page.")
            return redirect("accounts:login")
        if get_or_create_profile(request.user).role != Profile.Roles.EMPLOYER:
            messages.error(request, "This area is only available to employer accounts.")
            return _role_redirect(request)
        return view_func(request, *args, **kwargs)

    return _wrapped


def seeker_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please sign in to access that page.")
            return redirect("accounts:login")
        if get_or_create_profile(request.user).role != Profile.Roles.SEEKER:
            messages.error(request, "This area is only available to job seeker accounts.")
            return _role_redirect(request)
        return view_func(request, *args, **kwargs)

    return _wrapped
