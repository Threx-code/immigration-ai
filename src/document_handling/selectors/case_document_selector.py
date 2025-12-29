from document_handling.models.case_document import CaseDocument
from immigration_cases.models.case import Case


class CaseDocumentSelector:
    """Selector for CaseDocument read operations."""

    @staticmethod
    def get_all():
        """Get all case documents."""
        return CaseDocument.objects.select_related(
            'case',
            'case__user',
            'document_type'
        ).all().order_by('-uploaded_at')

    @staticmethod
    def get_by_case(case: Case):
        """Get documents by case."""
        return CaseDocument.objects.select_related(
            'case',
            'case__user',
            'document_type'
        ).filter(case=case).order_by('-uploaded_at')

    @staticmethod
    def get_by_status(status: str):
        """Get documents by status."""
        return CaseDocument.objects.select_related(
            'case',
            'case__user',
            'document_type'
        ).filter(status=status).order_by('-uploaded_at')

    @staticmethod
    def get_by_document_type(document_type_id):
        """Get documents by document type."""
        return CaseDocument.objects.select_related(
            'case',
            'case__user',
            'document_type'
        ).filter(document_type_id=document_type_id).order_by('-uploaded_at')

    @staticmethod
    def get_by_id(document_id):
        """Get case document by ID."""
        return CaseDocument.objects.select_related(
            'case',
            'case__user',
            'document_type'
        ).get(id=document_id)

    @staticmethod
    def get_verified_by_case(case: Case):
        """Get verified documents by case."""
        return CaseDocument.objects.select_related(
            'case',
            'case__user',
            'document_type'
        ).filter(case=case, status='verified').order_by('-uploaded_at')

