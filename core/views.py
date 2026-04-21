from django.contrib.auth.models import User
from django.shortcuts import render

from applications.models import Application
from jobs.models import Job


def home(request):
    featured_jobs = Job.objects.filter(is_active=True).select_related("employer__profile").order_by("-created_at")[:6]
    category_cards = [("Engineering", "Backend, frontend, DevOps, and data roles."), ("Design", "Product design, brand systems, and creative craft."), ("Marketing", "Growth, content, lifecycle, and digital strategy."), ("Product", "Product managers, analysts, and delivery leaders."), ("Operations", "People ops, finance ops, and business support."), ("Sales", "Revenue, partnerships, and customer acquisition.")]
    stats = {
        "active_jobs": Job.objects.filter(is_active=True).count(),
        "employers": User.objects.filter(profile__role="employer").count(),
        "applications": Application.objects.count(),
        "placements": Application.objects.filter(status="accepted").count(),
    }
    testimonials = [
        {"quote": "We filled three hard-to-hire roles in under a month with a much stronger candidate experience.", "name": "Maya Johnson", "title": "Talent Lead, Northstar Labs"},
        {"quote": "The dashboard makes it easy to review applicants without drowning in spreadsheets or email threads.", "name": "David Kim", "title": "Founder, Atlas Commerce"},
        {"quote": "Applying felt clear, fast, and professional. I always knew where my application stood.", "name": "Sara Patel", "title": "Senior Product Designer"},
    ]
    trusted_companies = ["Northstar Labs", "Atlas Commerce", "Pinehouse", "Lumen Works", "Brio Digital"]
    return render(request, "core/home.html", {"featured_jobs": featured_jobs, "category_cards": category_cards, "stats": stats, "testimonials": testimonials, "trusted_companies": trusted_companies})


def about(request):
    return render(request, "core/about.html")
