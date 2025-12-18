from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from users_access.models.user_profile import UserProfile


User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to automatically create UserProfile when a User is created.
    This ensures every user has a profile for GDPR-separated PII storage.
    """
    if created:
        # Create profile if it doesn't exist
        UserProfile.objects.get_or_create(user=instance)

