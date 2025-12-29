from django.utils import timezone
from rules_knowledge.models.visa_type import VisaType


class VisaTypeSelector:
    """Selector for VisaType read operations."""

    @staticmethod
    def get_all():
        """Get all visa types."""
        return VisaType.objects.all().order_by('jurisdiction', 'code')

    @staticmethod
    def get_active():
        """Get all active visa types."""
        return VisaType.objects.filter(is_active=True).order_by('jurisdiction', 'code')

    @staticmethod
    def get_by_jurisdiction(jurisdiction: str):
        """Get visa types by jurisdiction."""
        return VisaType.objects.filter(jurisdiction=jurisdiction, is_active=True).order_by('code')

    @staticmethod
    def get_by_code(jurisdiction: str, code: str):
        """Get visa type by jurisdiction and code."""
        return VisaType.objects.get(jurisdiction=jurisdiction, code=code)

    @staticmethod
    def get_by_id(type_id):
        """Get visa type by ID."""
        return VisaType.objects.select_related().get(id=type_id)

