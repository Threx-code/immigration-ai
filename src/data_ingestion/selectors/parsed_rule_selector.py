from data_ingestion.models.parsed_rule import ParsedRule


class ParsedRuleSelector:
    """Selector for ParsedRule read operations."""

    @staticmethod
    def get_all():
        """Get all parsed rules."""
        return ParsedRule.objects.select_related(
            'document_version',
            'document_version__source_document',
            'document_version__source_document__data_source'
        ).all()

    @staticmethod
    def get_by_status(status: str):
        """Get parsed rules by status."""
        return ParsedRule.objects.select_related(
            'document_version',
            'document_version__source_document',
            'document_version__source_document__data_source'
        ).filter(status=status).order_by('-created_at')

    @staticmethod
    def get_by_visa_code(visa_code: str):
        """Get parsed rules by visa code."""
        return ParsedRule.objects.select_related(
            'document_version',
            'document_version__source_document',
            'document_version__source_document__data_source'
        ).filter(visa_code=visa_code).order_by('-created_at')

    @staticmethod
    def get_by_document_version(document_version):
        """Get parsed rules by document version."""
        return ParsedRule.objects.select_related(
            'document_version',
            'document_version__source_document',
            'document_version__source_document__data_source'
        ).filter(document_version=document_version).order_by('-created_at')

    @staticmethod
    def get_pending():
        """Get all pending parsed rules."""
        return ParsedRule.objects.select_related(
            'document_version',
            'document_version__source_document',
            'document_version__source_document__data_source'
        ).filter(status='pending').order_by('-confidence_score', '-created_at')

    @staticmethod
    def get_by_id(rule_id):
        """Get parsed rule by ID."""
        return ParsedRule.objects.select_related(
            'document_version',
            'document_version__source_document',
            'document_version__source_document__data_source'
        ).get(id=rule_id)

