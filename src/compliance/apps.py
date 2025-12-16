from django.apps import AppConfig
from django.core.signals import request_started


class ComplianceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "compliance"


    def ready(self):
        from .handlers.logging_setup import LoggingSetup
        request_started.connect(LoggingSetup.safe_setup, dispatch_uid="audit-logs-init")

