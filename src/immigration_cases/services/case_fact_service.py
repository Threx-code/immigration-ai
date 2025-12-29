import logging
from typing import Optional
from immigration_cases.models.case_fact import CaseFact
from immigration_cases.repositories.case_fact_repository import CaseFactRepository
from immigration_cases.selectors.case_fact_selector import CaseFactSelector
from immigration_cases.selectors.case_selector import CaseSelector

logger = logging.getLogger('django')


class CaseFactService:
    """Service for CaseFact business logic."""

    @staticmethod
    def create_case_fact(case_id: str, fact_key: str, fact_value, source: str = 'user') -> Optional[CaseFact]:
        """Create a new case fact."""
        try:
            case = CaseSelector.get_by_id(case_id)
            return CaseFactRepository.create_case_fact(case, fact_key, fact_value, source)
        except Exception as e:
            logger.error(f"Error creating case fact: {e}")
            return None

    @staticmethod
    def get_all():
        """Get all case facts."""
        try:
            return CaseFactSelector.get_all()
        except Exception as e:
            logger.error(f"Error fetching all case facts: {e}")
            return CaseFact.objects.none()

    @staticmethod
    def get_by_case(case_id: str):
        """Get facts by case."""
        try:
            case = CaseSelector.get_by_id(case_id)
            return CaseFactSelector.get_by_case(case)
        except Exception as e:
            logger.error(f"Error fetching facts for case {case_id}: {e}")
            return CaseFact.objects.none()

    @staticmethod
    def get_by_id(fact_id: str) -> Optional[CaseFact]:
        """Get case fact by ID."""
        try:
            return CaseFactSelector.get_by_id(fact_id)
        except CaseFact.DoesNotExist:
            logger.error(f"Case fact {fact_id} not found")
            return None
        except Exception as e:
            logger.error(f"Error fetching case fact {fact_id}: {e}")
            return None

    @staticmethod
    def update_case_fact(fact_id: str, **fields) -> Optional[CaseFact]:
        """Update case fact fields."""
        try:
            fact = CaseFactSelector.get_by_id(fact_id)
            return CaseFactRepository.update_case_fact(fact, **fields)
        except CaseFact.DoesNotExist:
            logger.error(f"Case fact {fact_id} not found")
            return None
        except Exception as e:
            logger.error(f"Error updating case fact {fact_id}: {e}")
            return None

    @staticmethod
    def delete_case_fact(fact_id: str) -> bool:
        """Delete a case fact."""
        try:
            fact = CaseFactSelector.get_by_id(fact_id)
            CaseFactRepository.delete_case_fact(fact)
            return True
        except CaseFact.DoesNotExist:
            logger.error(f"Case fact {fact_id} not found")
            return False
        except Exception as e:
            logger.error(f"Error deleting case fact {fact_id}: {e}")
            return False

