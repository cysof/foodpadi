from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from .models import FarmPadiUser, Profile

@receiver(post_save, sender=FarmPadiUser)
def handle_user_profile(sender, instance, created, **kwargs):
    """
    Combined signal handler for both creation and updating of user profiles.
    """
    if created:
        # Create new profile for newly created user
         Profile.objects.create(user=instance, profile_type=instance.account_type)
    else:
        try:
            # Get existing profile
            profile = instance.profile
        except ObjectDoesNotExist:
            # Create profile if it doesn't exist (handles case where profile was deleted)
            Profile.objects.create(user=instance)