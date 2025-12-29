from immigration_cases.models.case import Case


class CaseSelector:
    """Selector for Case read operations."""

    @staticmethod
    def get_all():
        """Get all cases."""
        return Case.objects.select_related('user', 'user__profile').all().order_by('-created_at')

    @staticmethod
    def get_by_user(user):
        """Get cases by user."""
        return Case.objects.select_related('user', 'user__profile').filter(
            user=user
        ).order_by('-created_at')

    @staticmethod
    def get_by_status(status: str):
        """Get cases by status."""
        return Case.objects.select_related('user', 'user__profile').filter(
            status=status
        ).order_by('-created_at')

    @staticmethod
    def get_by_jurisdiction(jurisdiction: str):
        """Get cases by jurisdiction."""
        return Case.objects.select_related('user', 'user__profile').filter(
            jurisdiction=jurisdiction
        ).order_by('-created_at')

    @staticmethod
    def get_by_id(case_id):
        """Get case by ID."""
        return Case.objects.select_related('user', 'user__profile').get(id=case_id)

    @staticmethod
    def get_by_user_and_status(user, status: str):
        """Get cases by user and status."""
        return Case.objects.select_related('user', 'user__profile').filter(
            user=user,
            status=status
        ).order_by('-created_at')

