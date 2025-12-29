from document_handling.models.document_check import DocumentCheck
from document_handling.models.case_document import CaseDocument


class DocumentCheckSelector:
    """Selector for DocumentCheck read operations."""

    @staticmethod
    def get_all():
        """Get all document checks."""
        return DocumentCheck.objects.select_related(
            'case_document',
            'case_document__case',
            'case_document__document_type'
        ).all().order_by('-created_at')

    @staticmethod
    def get_by_case_document(case_document: CaseDocument):
        """Get checks by case document."""
        return DocumentCheck.objects.select_related(
            'case_document',
            'case_document__case',
            'case_document__document_type'
        ).filter(case_document=case_document).order_by('-created_at')

    @staticmethod
    def get_by_check_type(check_type: str):
        """Get checks by check type."""
        return DocumentCheck.objects.select_related(
            'case_document',
            'case_document__case',
            'case_document__document_type'
        ).filter(check_type=check_type).order_by('-created_at')

    @staticmethod
    def get_by_result(result: str):
        """Get checks by result."""
        return DocumentCheck.objects.select_related(
            'case_document',
            'case_document__case',
            'case_document__document_type'
        ).filter(result=result).order_by('-created_at')

    @staticmethod
    def get_by_id(check_id):
        """Get document check by ID."""
        return DocumentCheck.objects.select_related(
            'case_document',
            'case_document__case',
            'case_document__document_type'
        ).get(id=check_id)

    @staticmethod
    def get_latest_by_case_document(case_document: CaseDocument, check_type: str = None):
        """Get latest check for a case document, optionally filtered by check type."""
        queryset = DocumentCheck.objects.select_related(
            'case_document',
            'case_document__case',
            'case_document__document_type'
        ).filter(case_document=case_document)
        
        if check_type:
            queryset = queryset.filter(check_type=check_type)
        
        return queryset.order_by('-created_at').first()

