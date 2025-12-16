from django.apps import AppConfig
from django.core.signals import request_started



class LogEntryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "log_entry"

    def ready(self):
        from .logging_setup import LoggingSetup
        request_started.connect(LoggingSetup.safe_setup, dispatch_uid="log-entry-init")
