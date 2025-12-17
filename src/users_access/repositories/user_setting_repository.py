from typing import Dict
from django.db import transaction
from users_access.models.user_settings import UserSetting
from helpers.totp import TOTPAuthenticator

class UserSettingRepository:

    @staticmethod
    def create_user_setting(user_id: str):
        with transaction.atomic():
            settings = UserSetting(user_id=user_id)
            settings.full_clean()
            settings.save()
            return settings

    @staticmethod
    def update_settings(user_id: str, settings_data: Dict):
        with transaction.atomic():
            settings = UserSetting.objects.get(user__id=user_id)
            for key, value in settings_data.items():
                if hasattr(settings, key):
                    setattr(settings, key, value)
            settings.full_clean()
            settings.save()
            return settings

    @staticmethod
    def delete_settings(user_id: str):
        with transaction.atomic():
            settings = UserSetting.objects.get(user__id=user_id)
            settings.delete()
            return True

    @staticmethod
    def enable_2fa(user_id: str):
        with transaction.atomic():
            settings = UserSetting.objects.get(user__id=user_id)
            secret = TOTPAuthenticator.generate_totp()
            settings.two_factor_auth = True
            settings.totp_secret = secret
            settings.full_clean()
            settings.save()
            return settings
