from django.db import transaction
from django.utils import timezone
from rules_knowledge.models.visa_rule_version import VisaRuleVersion
from rules_knowledge.models.visa_type import VisaType


class VisaRuleVersionRepository:
    """Repository for VisaRuleVersion write operations."""

    @staticmethod
    def create_rule_version(visa_type: VisaType, effective_from, effective_to=None,
                           source_document_version=None, is_published: bool = False):
        """Create a new rule version."""
        with transaction.atomic():
            # Set effective_to on previous current version if exists
            if effective_to is None:
                previous_versions = VisaRuleVersion.objects.filter(
                    visa_type=visa_type,
                    effective_to__isnull=True
                )
                for prev_version in previous_versions:
                    prev_version.effective_to = effective_from
                    prev_version.save()
            
            rule_version = VisaRuleVersion.objects.create(
                visa_type=visa_type,
                effective_from=effective_from,
                effective_to=effective_to,
                source_document_version=source_document_version,
                is_published=is_published
            )
            rule_version.full_clean()
            rule_version.save()
            return rule_version

    @staticmethod
    def update_rule_version(rule_version, **fields):
        """Update rule version fields."""
        with transaction.atomic():
            for key, value in fields.items():
                if hasattr(rule_version, key):
                    setattr(rule_version, key, value)
            rule_version.full_clean()
            rule_version.save()
            return rule_version

    @staticmethod
    def publish_rule_version(rule_version):
        """Publish a rule version."""
        with transaction.atomic():
            rule_version.is_published = True
            rule_version.full_clean()
            rule_version.save()
            return rule_version

    @staticmethod
    def delete_rule_version(rule_version):
        """Delete a rule version."""
        with transaction.atomic():
            rule_version.delete()

