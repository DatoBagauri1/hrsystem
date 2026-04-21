from django.apps import apps
from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import get_or_create_profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        get_or_create_profile(instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not kwargs.get("raw", False):
        get_or_create_profile(instance)


@receiver(post_migrate)
def ensure_profiles_exist(sender, **kwargs):
    if sender.label != "accounts":
        return

    user_model = apps.get_model("auth", "User")
    for user in user_model.objects.filter(profile__isnull=True):
        get_or_create_profile(user)
