from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from .models import FarmPadiUser, Profile

@receiver(post_save, sender=FarmPadiUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler for creating a Profile when a new User is created.
    Automatically sets profile_type to match the user's selected account_type.
    Only runs when user is first created, not on updates.
    """
    if created:
        Profile.objects.get_or_create(
            user=instance,
            defaults={'profile_type': instance.account_type}
        )