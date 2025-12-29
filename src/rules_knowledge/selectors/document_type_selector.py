from rules_knowledge.models.document_type import DocumentType


class DocumentTypeSelector:
    """Selector for DocumentType read operations."""

    @staticmethod
    def get_all():
        """Get all document types."""
        return DocumentType.objects.all().order_by('code')

    @staticmethod
    def get_active():
        """Get all active document types."""
        return DocumentType.objects.filter(is_active=True).order_by('code')

    @staticmethod
    def get_by_code(code: str):
        """Get document type by code."""
        return DocumentType.objects.get(code=code)

    @staticmethod
    def get_by_id(type_id):
        """Get document type by ID."""
        return DocumentType.objects.get(id=type_id)

