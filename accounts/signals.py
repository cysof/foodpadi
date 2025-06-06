from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Profile

@receiver(post_save, sender=User)
def handle_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler for ensuring a Profile is created for every new User.
    Prevents duplicate profiles.
    """
    try:
        profile = instance.profile
    except ObjectDoesNotExist:
        # Only create a profile if one doesn't already exist
        Profile.objects.create(user=instance, profile_type=instance.account_type)