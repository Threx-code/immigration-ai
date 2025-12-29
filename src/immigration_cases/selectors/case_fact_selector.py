from immigration_cases.models.case_fact import CaseFact
from immigration_cases.models.case import Case


class CaseFactSelector:
    """Selector for CaseFact read operations."""

    @staticmethod
    def get_all():
        """Get all case facts."""
        return CaseFact.objects.select_related('case', 'case__user').all().order_by('-created_at')

    @staticmethod
    def get_by_case(case: Case):
        """Get facts by case."""
        return CaseFact.objects.select_related('case', 'case__user').filter(
            case=case
        ).order_by('-created_at')

    @staticmethod
    def get_by_fact_key(case: Case, fact_key: str):
        """Get facts by case and fact key."""
        return CaseFact.objects.select_related('case', 'case__user').filter(
            case=case,
            fact_key=fact_key
        ).order_by('-created_at')

    @staticmethod
    def get_latest_by_fact_key(case: Case, fact_key: str):
        """Get latest fact by case and fact key."""
        return CaseFact.objects.select_related('case', 'case__user').filter(
            case=case,
            fact_key=fact_key
        ).order_by('-created_at').first()

    @staticmethod
    def get_by_source(source: str):
        """Get facts by source."""
        return CaseFact.objects.select_related('case', 'case__user').filter(
            source=source
        ).order_by('-created_at')

    @staticmethod
    def get_by_id(fact_id):
        """Get case fact by ID."""
        return CaseFact.objects.select_related('case', 'case__user').get(id=fact_id)

