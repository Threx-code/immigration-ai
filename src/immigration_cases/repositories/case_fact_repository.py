from django.db import transaction
from immigration_cases.models.case_fact import CaseFact
from immigration_cases.models.case import Case


class CaseFactRepository:
    """Repository for CaseFact write operations."""

    @staticmethod
    def create_case_fact(case: Case, fact_key: str, fact_value, source: str = 'user'):
        """Create a new case fact."""
        with transaction.atomic():
            fact = CaseFact.objects.create(
                case=case,
                fact_key=fact_key,
                fact_value=fact_value,
                source=source
            )
            fact.full_clean()
            fact.save()
            return fact

    @staticmethod
    def update_case_fact(fact: CaseFact, **fields):
        """Update case fact fields."""
        with transaction.atomic():
            for key, value in fields.items():
                if hasattr(fact, key):
                    setattr(fact, key, value)
            fact.full_clean()
            fact.save()
            return fact

    @staticmethod
    def delete_case_fact(fact: CaseFact):
        """Delete a case fact."""
        with transaction.atomic():
            fact.delete()

