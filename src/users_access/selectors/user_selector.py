from users_access.models import User
from django.db.models import Count, Q


class UserSelector:

    @staticmethod
    def get_all():
        """Get all users with profile."""
        return User.objects.select_related('profile', 'profile__nationality', 'profile__state_province')

    @staticmethod
    def get_by_email(email: str):
        """Get user by email with profile."""
        return User.objects.select_related(
            'profile',
            'profile__nationality',
            'profile__state_province',
            'profile__state_province__country'
        ).filter(email__iexact=email).first()

    @staticmethod
    def email_exists(email: str) -> bool:
        """Check if email exists."""
        return User.objects.filter(email__iexact=email).exists()

    @staticmethod
    def get_by_id(user_id: str):
        """Get user by ID with profile."""
        return User.objects.select_related(
            'profile',
            'profile__nationality',
            'profile__state_province',
            'profile__state_province__country'
        ).get(id=user_id)

    @staticmethod
    def get_reviewers():
        """Get all active reviewers."""
        return User.objects.select_related('profile').filter(
            role='reviewer',
            is_active=True
        )

    @staticmethod
    def get_reviewer_round_robin():
        """Get next reviewer using round-robin (least recently assigned)."""
        return User.objects.select_related('profile').filter(
            role='reviewer',
            is_active=True
        ).order_by('last_assigned_at', 'created_at').first()

    @staticmethod
    def get_reviewer_by_workload():
        """Get reviewer with least active reviews (workload-based)."""
        from human_reviews.models import Review
        
        reviewers = User.objects.select_related('profile').filter(
            role='reviewer',
            is_active=True
        ).annotate(
            active_reviews_count=Count(
                'reviews',
                filter=Q(reviews__status__in=['in_progress', 'pending'])
            )
        ).order_by('active_reviews_count', 'last_assigned_at', 'created_at')
        
        return reviewers.first()

    @staticmethod
    def get_by_role(role: str):
        """Get all users by role."""
        return User.objects.select_related('profile').filter(role=role, is_active=True)

