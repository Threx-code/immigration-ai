from celery import shared_task
import logging
from main_system.tasks_base import BaseTaskWithMeta
from document_handling.selectors.case_document_selector import CaseDocumentSelector
from document_handling.services.case_document_service import CaseDocumentService
from document_handling.services.document_check_service import DocumentCheckService
from document_handling.services.ocr_service import OCRService
from document_handling.services.document_classification_service import DocumentClassificationService

logger = logging.getLogger('django')


@shared_task(bind=True, base=BaseTaskWithMeta)
def process_document_task(self, document_id: str):
    """
    Celery task to process a document (OCR, classification, validation).
    
    This implements the workflow from implementation.md Section 8:
    1. OCR Extraction → Store text
    2. AI Classification → Update document_type_id
    3. Requirement Matching → Validate against visa requirements
    
    Args:
        document_id: UUID of the document to process
        
    Returns:
        Dict with processing results
    """
    try:
        logger.info(f"Starting document processing for document: {document_id}")
        
        # Update status to processing
        CaseDocumentService.update_case_document(
            document_id=document_id,
            status='processing'
        )
        
        document = CaseDocumentSelector.get_by_id(document_id)
        if not document:
            logger.error(f"Document {document_id} not found")
            return {'success': False, 'error': 'Document not found'}
        
        # Step 1: OCR Processing
        logger.info(f"Step 1: Running OCR for document {document_id}")
        ocr_text, ocr_metadata, ocr_error = OCRService.extract_text(
            file_path=document.file_path,
            mime_type=document.mime_type
        )
        
        ocr_result = 'passed'
        ocr_details = {'metadata': ocr_metadata} if ocr_metadata else {}
        
        if ocr_error or not ocr_text:
            ocr_result = 'failed'
            ocr_details['error'] = ocr_error or 'OCR extracted no text'
            logger.warning(f"OCR failed for document {document_id}: {ocr_error}")
        else:
            # Store OCR text in document
            CaseDocumentService.update_case_document(
                document_id=document_id,
                ocr_text=ocr_text
            )
            logger.info(f"OCR successful: {len(ocr_text)} characters extracted")
        
        # Create OCR check
        ocr_check = DocumentCheckService.create_document_check(
            case_document_id=document_id,
            check_type='ocr',
            result=ocr_result,
            details=ocr_details,
            performed_by='OCR Service'
        )
        
        # Step 2: Document Classification (only if OCR succeeded)
        classification_check = None
        if ocr_text and len(ocr_text.strip()) > 10:
            logger.info(f"Step 2: Classifying document {document_id}")
            
            document_type_id, confidence, classification_metadata, classification_error = \
                DocumentClassificationService.classify_document(
                    ocr_text=ocr_text,
                    file_name=document.file_name,
                    file_size=document.file_size,
                    mime_type=document.mime_type
                )
            
            classification_result = 'passed'
            classification_details = {
                'confidence': confidence,
                'metadata': classification_metadata or {}
            }
            
            if classification_error or not document_type_id:
                classification_result = 'failed'
                classification_details['error'] = classification_error or 'Classification failed'
                logger.warning(f"Classification failed for document {document_id}: {classification_error}")
            else:
                # Update document type if confidence is high enough
                should_auto_classify = DocumentClassificationService.should_auto_classify(confidence)
                
                if should_auto_classify:
                    # Auto-update document type
                    CaseDocumentService.update_case_document(
                        document_id=document_id,
                        document_type_id=document_type_id,
                        classification_confidence=confidence
                    )
                    logger.info(
                        f"Document type auto-updated to {document_type_id} "
                        f"(confidence: {confidence:.2f})"
                    )
                else:
                    # Low confidence - flag for human review
                    classification_result = 'warning'
                    classification_details['requires_review'] = True
                    classification_details['message'] = f"Low confidence ({confidence:.2f}), requires human review"
                    logger.info(
                        f"Classification confidence too low ({confidence:.2f}), "
                        f"flagging for human review"
                    )
            
            # Create classification check
            classification_check = DocumentCheckService.create_document_check(
                case_document_id=document_id,
                check_type='classification',
                result=classification_result,
                details=classification_details,
                performed_by='AI Classification Service'
            )
        else:
            logger.warning(f"Skipping classification for document {document_id}: insufficient OCR text")
            classification_check = DocumentCheckService.create_document_check(
                case_document_id=document_id,
                check_type='classification',
                result='pending',
                details={'reason': 'Insufficient OCR text for classification'},
                performed_by='AI Classification Service'
            )
        
        # Step 3: Requirement Matching (placeholder - implement based on visa requirements)
        # TODO: Implement requirement matching against visa_document_requirements
        requirement_check = DocumentCheckService.create_document_check(
            case_document_id=document_id,
            check_type='validation',
            result='pending',  # Will be implemented later
            details={'message': 'Requirement matching not yet implemented'},
            performed_by='Validation Service'
        )
        
        # Step 4: Update document status based on checks
        # Status = 'verified' if all critical checks pass
        # Status = 'rejected' if any critical check fails
        # Status = 'needs_attention' if warnings or pending checks
        
        critical_checks_passed = (
            ocr_check and ocr_check.result == 'passed' and
            classification_check and classification_check.result in ['passed', 'warning']
        )
        
        has_failures = (
            (ocr_check and ocr_check.result == 'failed') or
            (classification_check and classification_check.result == 'failed')
        )
        
        if has_failures:
            final_status = 'rejected'
        elif critical_checks_passed:
            final_status = 'verified'
        else:
            final_status = 'needs_attention'
        
        CaseDocumentService.update_case_document(
            document_id=document_id,
            status=final_status
        )
        
        logger.info(
            f"Document processing completed for document {document_id}: "
            f"status={final_status}, ocr={ocr_result}, classification={classification_check.result if classification_check else 'N/A'}"
        )
        
        return {
            'success': True,
            'document_id': document_id,
            'status': final_status,
            'ocr_check': str(ocr_check.id) if ocr_check else None,
            'classification_check': str(classification_check.id) if classification_check else None,
            'requirement_check': str(requirement_check.id) if requirement_check else None,
            'ocr_text_length': len(ocr_text) if ocr_text else 0,
            'classification_confidence': classification_check.details.get('confidence') if classification_check and classification_check.details else None
        }
        
    except Exception as e:
        logger.error(f"Error processing document {document_id}: {e}", exc_info=True)
        # Update status to indicate failure
        try:
            CaseDocumentService.update_case_document(
                document_id=document_id,
                status='needs_attention'
            )
        except:
            pass
        raise self.retry(exc=e, countdown=60, max_retries=3)

