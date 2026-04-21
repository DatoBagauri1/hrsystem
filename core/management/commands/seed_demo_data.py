import random
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from applications.models import Application
from jobs.models import Job


class Command(BaseCommand):
    help = "Create demo employers, job seekers, jobs, and applications."

    def handle(self, *args, **options):
        employer_specs = [
            {"username": "employer1", "email": "employer1@example.com", "company_name": "Northstar Labs", "location": "Tbilisi, Georgia", "website": "https://northstarlabs.example.com", "company_description": "A growth-stage product engineering company focused on modern SaaS experiences."},
            {"username": "employer2", "email": "employer2@example.com", "company_name": "Atlas Commerce", "location": "Remote", "website": "https://atlascommerce.example.com", "company_description": "A distributed commerce infrastructure team building tools for international retail brands."},
        ]
        seeker_specs = [
            {"username": "seeker1", "email": "seeker1@example.com", "full_name": "Nina Carter", "phone": "+995 555 000 111", "city": "Tbilisi", "skills": "Python, Django, PostgreSQL, Tailwind CSS", "experience_summary": "4 years building internal platforms and customer-facing web apps."},
            {"username": "seeker2", "email": "seeker2@example.com", "full_name": "Leo Anderson", "phone": "+995 555 000 222", "city": "Batumi", "skills": "Figma, Product Design, Design Systems, Prototyping", "experience_summary": "5 years designing user journeys for B2B SaaS products."},
        ]
        password = "DemoPass123!"
        employers = []
        for spec in employer_specs:
            user, created = User.objects.get_or_create(username=spec["username"], defaults={"email": spec["email"]})
            if created:
                user.set_password(password)
                user.email = spec["email"]
                user.save()
            profile = user.profile
            profile.role = "employer"
            profile.company_name = spec["company_name"]
            profile.location = spec["location"]
            profile.website = spec["website"]
            profile.company_description = spec["company_description"]
            profile.contact_email = spec["email"]
            profile.save()
            employers.append(user)
        seekers = []
        for spec in seeker_specs:
            user, created = User.objects.get_or_create(username=spec["username"], defaults={"email": spec["email"]})
            if created:
                user.set_password(password)
                user.email = spec["email"]
                user.save()
            profile = user.profile
            profile.role = "seeker"
            profile.full_name = spec["full_name"]
            profile.phone = spec["phone"]
            profile.city = spec["city"]
            profile.bio = "Actively exploring ambitious teams with strong product culture."
            profile.skills = spec["skills"]
            profile.experience_summary = spec["experience_summary"]
            profile.save()
            seekers.append(user)
        job_specs = [("Senior Django Engineer", "engineering", "full-time", "senior"), ("Product Designer", "design", "remote", "mid"), ("Growth Marketing Lead", "marketing", "full-time", "senior"), ("People Operations Specialist", "human-resources", "hybrid", "mid"), ("Junior QA Analyst", "engineering", "internship", "junior"), ("Partnerships Manager", "sales", "contract", "mid")]
        jobs = []
        for index, spec in enumerate(job_specs):
            employer = employers[index % len(employers)]
            title, category, job_type, experience = spec
            job, _ = Job.objects.get_or_create(employer=employer, title=title, company_name=employer.profile.company_name, defaults={"location": employer.profile.location or "Remote", "job_type": job_type, "category": category, "salary_min": 1800 + (index * 400), "salary_max": 2600 + (index * 500), "currency": "USD", "description": f"{title} role focused on high-impact delivery, strong collaboration, and thoughtful craft.", "requirements": "Relevant experience, strong communication, ownership mindset, and curiosity.", "responsibilities": "Own day-to-day execution, collaborate cross-functionally, and help improve team systems.", "benefits": "Flexible schedule, mentorship, learning budget, and modern tooling.", "experience_level": experience, "application_deadline": timezone.localdate() + timedelta(days=20 + index), "is_active": True})
            jobs.append(job)
        for seeker in seekers:
            for job in random.sample(jobs, k=3):
                if job.employer == seeker:
                    continue
                Application.objects.get_or_create(job=job, applicant=seeker, defaults={"full_name": seeker.profile.full_name or seeker.username, "email": seeker.email, "phone": seeker.profile.phone or "+995 555 000 000", "cover_letter": "I would love to contribute my experience and bring a thoughtful, collaborative approach to this role.", "status": random.choice(["pending", "reviewed", "shortlisted", "accepted", "rejected"])})
        self.stdout.write(self.style.SUCCESS("Demo data created successfully."))
        self.stdout.write("Employer credentials: employer1 / DemoPass123!, employer2 / DemoPass123!")
        self.stdout.write("Seeker credentials: seeker1 / DemoPass123!, seeker2 / DemoPass123!")
