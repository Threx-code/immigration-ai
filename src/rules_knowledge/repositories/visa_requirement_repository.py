from django.db import transaction
from rules_knowledge.models.visa_requirement import VisaRequirement
from rules_knowledge.models.visa_rule_version import VisaRuleVersion


class VisaRequirementRepository:
    """Repository for VisaRequirement write operations."""

    @staticmethod
    def create_requirement(rule_version: VisaRuleVersion, requirement_code: str, rule_type: str,
                          description: str, condition_expression: dict, is_mandatory: bool = True):
        """Create a new visa requirement."""
        with transaction.atomic():
            requirement = VisaRequirement.objects.create(
                rule_version=rule_version,
                requirement_code=requirement_code,
                rule_type=rule_type,
                description=description,
                condition_expression=condition_expression,
                is_mandatory=is_mandatory
            )
            requirement.full_clean()
            requirement.save()
            return requirement

    @staticmethod
    def update_requirement(requirement, **fields):
        """Update requirement fields."""
        with transaction.atomic():
            for key, value in fields.items():
                if hasattr(requirement, key):
                    setattr(requirement, key, value)
            requirement.full_clean()
            requirement.save()
            return requirement

    @staticmethod
    def delete_requirement(requirement):
        """Delete a requirement."""
        with transaction.atomic():
            requirement.delete()

