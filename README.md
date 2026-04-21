# TalentBridge Job Platform

TalentBridge is a traditional full-stack Django employment platform with two role-based experiences:

- Employers can register, manage only their own vacancies, review incoming applications, and update application status.
- Job seekers can register, complete their profile, browse vacancies, filter/search jobs, apply once per role, and track their application history.

The project is intentionally built with classic Django primitives:

- Django templates
- Django views
- Django models
- Django forms / ModelForms
- Django authentication
- Django messages framework
- SQLite
- Static and media configuration

## Features

- Role-based registration with automatic profile creation
- Employer and seeker dashboards
- Job CRUD with strict ownership rules
- Vacancy search, filtering, sorting, and pagination
- Application workflow with duplicate prevention
- Employer-side status management: `pending`, `reviewed`, `shortlisted`, `rejected`, `accepted`
- Public homepage, about page, and employer profile pages
- Polished Bootstrap 5 + custom CSS UI
- Admin configuration for all core models
- Demo data management command
- Basic automated tests for permissions and application flow

## Project Structure

```text
job_platform/
accounts/
applications/
core/
jobs/
templates/
static/
media/
```

## Installation

1. Create and activate a virtual environment.
2. Install dependencies.
3. Run migrations.
4. Create a superuser if needed.
5. Optionally seed demo data.
6. Start the development server.

## Exact Commands

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo_data
python manage.py runserver
```

macOS/Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo_data
python manage.py runserver
```

## URLs

- Home: `/`
- About: `/about/`
- Jobs: `/jobs/`
- Job detail: `/jobs/<slug>/`
- Create vacancy: `/jobs/create/`
- Edit vacancy: `/jobs/<slug>/edit/`
- Delete vacancy: `/jobs/<slug>/delete/`
- Apply to job: `/jobs/<slug>/apply/`
- Applicants for job: `/jobs/<slug>/applicants/`
- Employer dashboard: `/dashboard/employer/`
- Seeker dashboard: `/dashboard/seeker/`
- My applications: `/applications/`
- Application detail: `/applications/<id>/`
- Register: `/accounts/register/`
- Login: `/accounts/login/`
- Profile edit: `/accounts/profile/edit/`

## Demo Credentials

If you run `python manage.py seed_demo_data`, the command creates these users with password `demo12345`:

- Employer: `employer_alpha`
- Employer: `employer_nova`
- Seeker: `seeker_anna`
- Seeker: `seeker_liam`
- Seeker: `seeker_maya`

## Media and Static Files

- Static files live in `static/`
- Media uploads are stored in `media/`
- In development, Django serves media and static files when `DEBUG=True`

## Superuser Creation

```bash
python manage.py createsuperuser
```

Then visit `/admin/`.

## Tests

Run the automated test suite with:

```bash
python manage.py test
```

## Notes

- SQLite is used by default for quick local setup.
- Profiles are created automatically through Django signals.
- Permission checks are enforced server-side in views, not only in templates.
