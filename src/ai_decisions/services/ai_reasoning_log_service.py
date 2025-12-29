import logging
from typing import Optional
from ai_decisions.models.ai_reasoning_log import AIReasoningLog
from ai_decisions.repositories.ai_reasoning_log_repository import AIReasoningLogRepository
from ai_decisions.selectors.ai_reasoning_log_selector import AIReasoningLogSelector
from immigration_cases.selectors.case_selector import CaseSelector

logger = logging.getLogger('django')


class AIReasoningLogService:
    """Service for AIReasoningLog business logic."""

    @staticmethod
    def create_reasoning_log(case_id: str, prompt: str, response: str, model_name: str,
                            tokens_used: int = None) -> Optional[AIReasoningLog]:
        """Create a new AI reasoning log."""
        try:
            case = CaseSelector.get_by_id(case_id)
            return AIReasoningLogRepository.create_reasoning_log(
                case=case,
                prompt=prompt,
                response=response,
                model_name=model_name,
                tokens_used=tokens_used
            )
        except Exception as e:
            logger.error(f"Error creating AI reasoning log: {e}")
            return None

    @staticmethod
    def get_all():
        """Get all AI reasoning logs."""
        try:
            return AIReasoningLogSelector.get_all()
        except Exception as e:
            logger.error(f"Error fetching all AI reasoning logs: {e}")
            return AIReasoningLog.objects.none()

    @staticmethod
    def get_by_case(case_id: str):
        """Get reasoning logs by case."""
        try:
            case = CaseSelector.get_by_id(case_id)
            return AIReasoningLogSelector.get_by_case(case)
        except Exception as e:
            logger.error(f"Error fetching reasoning logs for case {case_id}: {e}")
            return AIReasoningLog.objects.none()

    @staticmethod
    def get_by_id(log_id: str) -> Optional[AIReasoningLog]:
        """Get reasoning log by ID."""
        try:
            return AIReasoningLogSelector.get_by_id(log_id)
        except AIReasoningLog.DoesNotExist:
            logger.error(f"AI reasoning log {log_id} not found")
            return None
        except Exception as e:
            logger.error(f"Error fetching reasoning log {log_id}: {e}")
            return None

    @staticmethod
    def update_reasoning_log(log_id: str, **fields) -> Optional[AIReasoningLog]:
        """Update reasoning log fields."""
        try:
            log = AIReasoningLogSelector.get_by_id(log_id)
            return AIReasoningLogRepository.update_reasoning_log(log, **fields)
        except AIReasoningLog.DoesNotExist:
            logger.error(f"AI reasoning log {log_id} not found")
            return None
        except Exception as e:
            logger.error(f"Error updating reasoning log {log_id}: {e}")
            return None

    @staticmethod
    def delete_reasoning_log(log_id: str) -> bool:
        """Delete an AI reasoning log."""
        try:
            log = AIReasoningLogSelector.get_by_id(log_id)
            AIReasoningLogRepository.delete_reasoning_log(log)
            return True
        except AIReasoningLog.DoesNotExist:
            logger.error(f"AI reasoning log {log_id} not found")
            return False
        except Exception as e:
            logger.error(f"Error deleting reasoning log {log_id}: {e}")
            return False

