from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FarmPadiUser, Profile

@receiver(post_save, sender=FarmPadiUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, profile_type=instance.account_type)

@receiver(post_save, sender=FarmPadiUser)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
