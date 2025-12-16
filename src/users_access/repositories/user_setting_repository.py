from typing import Dict
from django.db import models
import logging

from helpers.totp import TOTPAuthenticator

logger = logging.getLogger('django')

class UserSettingsManager(models.Manager):

    def create_user_setting(self, user_id: str):
        try:
            return self.create(user_id=user_id)
        except Exception as e:
            logger.error(f"Error while creating default settings for user {user_id}: {e}")
        return None

    def update_settings(self, user_id: str, settings_data: Dict):
        try:
            settings = self.get_queryset().get(user__id=user_id)
            for key, value in settings_data.items():
                if hasattr(settings, key):
                    setattr(settings, key, value)
            settings.save()
            return settings
        except Exception as e:
            logger.error(f"Error while updating settings for user {user_id}: {e}")
        return None

    def get_settings(self, user_id: str):
        try:
            user_settings = self.get_queryset().get(user__id=user_id)
            if not user_settings:
                logger.error(f"Settings not found for user {user_id}")
                return None
            logger.info(f"Settings fetched for user {user_id}: {user_settings}")
            return user_settings
        except Exception as e:
            logger.error(f"Error while fetching settings for user {user_id}: {e}")
            return None
    def delete_settings(self, user_id: str):
        try:
            settings = self.get_queryset().get(user__id=user_id)
            if not settings:
                logger.error(f"Settings not found for user {user_id}")
                return False
            settings.delete()
            logger.info(f"Settings deleted for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error while deleting settings for user {user_id}: {e}")
            return False

    def enable_2fa(self, user_id: str):
        try:
            secret = TOTPAuthenticator.generate_totp()
            settings = self.get_queryset().get(user__id=user_id)
            if not settings:
                logger.error(f"Settings not found for user {user_id}")
                return None
            # If the user already has 2FA enabled, we can skip enabling it again
            if settings.two_factor_auth and settings.totp_secret:
                logger.warning(f"2FA already enabled for user {user_id}")
                return settings

            settings.two_factor_auth = True
            settings.totp_secret = secret
            settings.save()

            logger.info(f"2FA enabled for user {user_id} with secret {secret}")
            return settings
        except Exception as e:
            logger.error(f"Error while enabling 2FA for user {user_id}: {e}")
        return None