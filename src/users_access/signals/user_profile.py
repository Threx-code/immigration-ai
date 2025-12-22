from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from users_access.services.user_profile_service import UserProfileService


User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to automatically create UserProfile when a User is created.
    This ensures every user has a profile for GDPR-separated PII storage.
    """
    if created:
        # Create profile if it doesn't exist (service handles existence check)
        UserProfileService.get_profile(user=instance)

