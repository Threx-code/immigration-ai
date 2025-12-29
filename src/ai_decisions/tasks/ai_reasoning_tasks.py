from celery import shared_task
import logging
from main_system.tasks_base import BaseTaskWithMeta
from ai_decisions.services.eligibility_result_service import EligibilityResultService
from immigration_cases.selectors.case_selector import CaseSelector
from rules_knowledge.selectors.visa_type_selector import VisaTypeSelector

logger = logging.getLogger('django')


@shared_task(bind=True, base=BaseTaskWithMeta)
def run_eligibility_check_task(self, case_id: str, visa_type_id: str = None):
    """
    Celery task to run eligibility check for a case.
    This runs the rule engine + AI reasoning asynchronously.
    
    Args:
        case_id: UUID of the case
        visa_type_id: Optional visa type ID to check (if None, checks all active visa types)
        
    Returns:
        Dict with eligibility results
    """
    try:
        logger.info(f"Starting eligibility check for case: {case_id}, visa_type: {visa_type_id}")
        
        case = CaseSelector.get_by_id(case_id)
        if not case:
            logger.error(f"Case {case_id} not found")
            return {'success': False, 'error': 'Case not found'}
        
        # If visa_type_id provided, check only that visa type
        if visa_type_id:
            visa_type = VisaTypeSelector.get_by_id(visa_type_id)
            if not visa_type:
                logger.error(f"Visa type {visa_type_id} not found")
                return {'success': False, 'error': 'Visa type not found'}
            
            # Run eligibility check for this visa type
            # This is a placeholder - implement actual rule engine + AI reasoning
            # For now, we'll create a basic eligibility result
            result = EligibilityResultService.create_eligibility_result(
                case_id=case_id,
                visa_type_id=visa_type_id,
                rule_version_id=None,  # Get active rule version
                outcome='requires_review',  # Placeholder
                confidence=0.5,  # Placeholder
                reasoning_summary='Eligibility check completed. Review required.',
                missing_facts=None
            )
            
            return {
                'success': True,
                'case_id': case_id,
                'visa_type_id': visa_type_id,
                'result_id': str(result.id) if result else None
            }
        else:
            # Check all active visa types for the jurisdiction
            # This is a placeholder - implement actual logic
            logger.info(f"Checking all visa types for case {case_id}")
            return {
                'success': True,
                'case_id': case_id,
                'message': 'Eligibility check initiated for all visa types'
            }
        
    except Exception as e:
        logger.error(f"Error running eligibility check for case {case_id}: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)

