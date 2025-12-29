from django.utils import timezone
from django.db import models
from rules_knowledge.models.visa_rule_version import VisaRuleVersion
from rules_knowledge.models.visa_type import VisaType


class VisaRuleVersionSelector:
    """Selector for VisaRuleVersion read operations."""

    @staticmethod
    def get_all():
        """Get all rule versions."""
        return VisaRuleVersion.objects.select_related(
            'visa_type',
            'source_document_version',
            'source_document_version__source_document'
        ).all().order_by('-effective_from')

    @staticmethod
    def get_by_visa_type(visa_type: VisaType):
        """Get rule versions by visa type."""
        return VisaRuleVersion.objects.select_related(
            'visa_type',
            'source_document_version',
            'source_document_version__source_document'
        ).filter(visa_type=visa_type).order_by('-effective_from')

    @staticmethod
    def get_current_by_visa_type(visa_type: VisaType):
        """Get current rule version for a visa type."""
        now = timezone.now()
        return VisaRuleVersion.objects.select_related(
            'visa_type',
            'source_document_version',
            'source_document_version__source_document'
        ).filter(
            visa_type=visa_type,
            effective_from__lte=now,
            is_published=True
        ).filter(
            models.Q(effective_to__isnull=True) | models.Q(effective_to__gte=now)
        ).order_by('-effective_from').first()

    @staticmethod
    def get_published():
        """Get all published rule versions."""
        return VisaRuleVersion.objects.select_related(
            'visa_type',
            'source_document_version',
            'source_document_version__source_document'
        ).filter(is_published=True).order_by('-effective_from')

    @staticmethod
    def get_by_id(version_id):
        """Get rule version by ID."""
        return VisaRuleVersion.objects.select_related(
            'visa_type',
            'source_document_version',
            'source_document_version__source_document'
        ).get(id=version_id)

