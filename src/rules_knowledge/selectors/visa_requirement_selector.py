from rules_knowledge.models.visa_requirement import VisaRequirement
from rules_knowledge.models.visa_rule_version import VisaRuleVersion


class VisaRequirementSelector:
    """Selector for VisaRequirement read operations."""

    @staticmethod
    def get_all():
        """Get all requirements."""
        return VisaRequirement.objects.select_related(
            'rule_version',
            'rule_version__visa_type'
        ).all().order_by('requirement_code')

    @staticmethod
    def get_by_rule_version(rule_version: VisaRuleVersion):
        """Get requirements by rule version."""
        return VisaRequirement.objects.select_related(
            'rule_version',
            'rule_version__visa_type'
        ).filter(rule_version=rule_version).order_by('requirement_code')

    @staticmethod
    def get_mandatory_by_rule_version(rule_version: VisaRuleVersion):
        """Get mandatory requirements by rule version."""
        return VisaRequirement.objects.select_related(
            'rule_version',
            'rule_version__visa_type'
        ).filter(rule_version=rule_version, is_mandatory=True).order_by('requirement_code')

    @staticmethod
    def get_by_rule_type(rule_type: str):
        """Get requirements by rule type."""
        return VisaRequirement.objects.select_related(
            'rule_version',
            'rule_version__visa_type'
        ).filter(rule_type=rule_type).order_by('requirement_code')

    @staticmethod
    def get_by_id(requirement_id):
        """Get requirement by ID."""
        return VisaRequirement.objects.select_related(
            'rule_version',
            'rule_version__visa_type'
        ).get(id=requirement_id)

