from django.apps import AppConfig


class DocumentHandlingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "document_handling"

    def ready(self):
        from .signals import document_signals
