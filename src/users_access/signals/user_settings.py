from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from users_access.services.user_setting_service import UserSettingsService


User = get_user_model()

@receiver(post_save, sender=User)
def create_user_setting(sender, instance, created, **kwargs):
    """Signal to automatically create UserSetting when a User is created."""
    if created:
        UserSettingsService.create_user_setting(user=instance)
