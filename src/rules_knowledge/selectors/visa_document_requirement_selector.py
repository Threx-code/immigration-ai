from rules_knowledge.models.visa_document_requirement import VisaDocumentRequirement
from rules_knowledge.models.visa_rule_version import VisaRuleVersion
from rules_knowledge.models.document_type import DocumentType


class VisaDocumentRequirementSelector:
    """Selector for VisaDocumentRequirement read operations."""

    @staticmethod
    def get_all():
        """Get all document requirements."""
        return VisaDocumentRequirement.objects.select_related(
            'rule_version',
            'rule_version__visa_type',
            'document_type'
        ).all()

    @staticmethod
    def get_by_rule_version(rule_version: VisaRuleVersion):
        """Get document requirements by rule version."""
        return VisaDocumentRequirement.objects.select_related(
            'rule_version',
            'rule_version__visa_type',
            'document_type'
        ).filter(rule_version=rule_version).order_by('document_type__code')

    @staticmethod
    def get_mandatory_by_rule_version(rule_version: VisaRuleVersion):
        """Get mandatory document requirements by rule version."""
        return VisaDocumentRequirement.objects.select_related(
            'rule_version',
            'rule_version__visa_type',
            'document_type'
        ).filter(rule_version=rule_version, mandatory=True).order_by('document_type__code')

    @staticmethod
    def get_by_document_type(document_type: DocumentType):
        """Get document requirements by document type."""
        return VisaDocumentRequirement.objects.select_related(
            'rule_version',
            'rule_version__visa_type',
            'document_type'
        ).filter(document_type=document_type)

    @staticmethod
    def get_by_id(requirement_id):
        """Get document requirement by ID."""
        return VisaDocumentRequirement.objects.select_related(
            'rule_version',
            'rule_version__visa_type',
            'document_type'
        ).get(id=requirement_id)

