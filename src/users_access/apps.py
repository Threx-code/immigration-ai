from django.apps import AppConfig


class PasswordResetConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users_access"

    def ready(self):
        import otp.tasks
        from .signals import user_settings
