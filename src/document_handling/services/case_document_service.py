import logging
from typing import Optional
from document_handling.models.case_document import CaseDocument
from document_handling.repositories.case_document_repository import CaseDocumentRepository
from document_handling.selectors.case_document_selector import CaseDocumentSelector
from immigration_cases.selectors.case_selector import CaseSelector
from immigration_cases.models.case import Case
from rules_knowledge.selectors.document_type_selector import DocumentTypeSelector

logger = logging.getLogger('django')


class CaseDocumentService:
    """Service for CaseDocument business logic."""

    @staticmethod
    def create_case_document(case_id: str, document_type_id: str, file_path: str,
                            file_name: str, file_size: int = None, mime_type: str = None,
                            status: str = 'uploaded'):
        """Create a new case document."""
        try:
            # Get case
            case = CaseSelector.get_by_id(case_id)
            
            # Get document type
            document_type = DocumentTypeSelector.get_by_id(document_type_id)
            if not document_type.is_active:
                logger.error(f"Document type {document_type_id} is not active")
                return None
            
            return CaseDocumentRepository.create_case_document(
                case=case,
                document_type=document_type,
                file_path=file_path,
                file_name=file_name,
                file_size=file_size,
                mime_type=mime_type,
                status=status
            )
        except Case.DoesNotExist:
            logger.error(f"Case {case_id} not found")
            return None
        except Exception as e:
            logger.error(f"Error creating case document: {e}")
            return None

    @staticmethod
    def get_all():
        """Get all case documents."""
        try:
            return CaseDocumentSelector.get_all()
        except Exception as e:
            logger.error(f"Error fetching all case documents: {e}")
            return CaseDocument.objects.none()

    @staticmethod
    def get_by_case(case_id: str):
        """Get documents by case."""
        try:
            case = CaseSelector.get_by_id(case_id)
            return CaseDocumentSelector.get_by_case(case)
        except Case.DoesNotExist:
            logger.error(f"Case {case_id} not found")
            return CaseDocument.objects.none()
        except Exception as e:
            logger.error(f"Error fetching documents for case {case_id}: {e}")
            return CaseDocument.objects.none()

    @staticmethod
    def get_by_status(status: str):
        """Get documents by status."""
        try:
            return CaseDocumentSelector.get_by_status(status)
        except Exception as e:
            logger.error(f"Error fetching documents by status {status}: {e}")
            return CaseDocument.objects.none()

    @staticmethod
    def get_by_document_type(document_type_id: str):
        """Get documents by document type."""
        try:
            return CaseDocumentSelector.get_by_document_type(document_type_id)
        except Exception as e:
            logger.error(f"Error fetching documents by document type {document_type_id}: {e}")
            return CaseDocument.objects.none()

    @staticmethod
    def get_by_id(document_id: str) -> Optional[CaseDocument]:
        """Get case document by ID."""
        try:
            return CaseDocumentSelector.get_by_id(document_id)
        except CaseDocument.DoesNotExist:
            logger.error(f"Case document {document_id} not found")
            return None
        except Exception as e:
            logger.error(f"Error fetching case document {document_id}: {e}")
            return None

    @staticmethod
    def update_case_document(document_id: str, **fields) -> Optional[CaseDocument]:
        """Update case document."""
        try:
            case_document = CaseDocumentSelector.get_by_id(document_id)
            return CaseDocumentRepository.update_case_document(case_document, **fields)
        except CaseDocument.DoesNotExist:
            logger.error(f"Case document {document_id} not found")
            return None
        except Exception as e:
            logger.error(f"Error updating case document {document_id}: {e}")
            return None

    @staticmethod
    def update_status(document_id: str, status: str) -> Optional[CaseDocument]:
        """Update document status."""
        try:
            case_document = CaseDocumentSelector.get_by_id(document_id)
            return CaseDocumentRepository.update_status(case_document, status)
        except CaseDocument.DoesNotExist:
            logger.error(f"Case document {document_id} not found")
            return None
        except Exception as e:
            logger.error(f"Error updating document status {document_id}: {e}")
            return None

    @staticmethod
    def delete_case_document(document_id: str) -> bool:
        """Delete case document."""
        try:
            case_document = CaseDocumentSelector.get_by_id(document_id)
            CaseDocumentRepository.delete_case_document(case_document)
            return True
        except CaseDocument.DoesNotExist:
            logger.error(f"Case document {document_id} not found")
            return False
        except Exception as e:
            logger.error(f"Error deleting case document {document_id}: {e}")
            return False

    @staticmethod
    def get_verified_by_case(case_id: str):
        """Get verified documents by case."""
        try:
            case = CaseSelector.get_by_id(case_id)
            return CaseDocumentSelector.get_verified_by_case(case)
        except Case.DoesNotExist:
            logger.error(f"Case {case_id} not found")
            return CaseDocument.objects.none()
        except Exception as e:
            logger.error(f"Error fetching verified documents for case {case_id}: {e}")
            return CaseDocument.objects.none()

