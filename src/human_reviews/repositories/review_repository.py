from django.db import transaction
from django.utils import timezone
from human_reviews.models.review import Review
from immigration_cases.models.case import Case
from django.conf import settings


class ReviewRepository:
    """Repository for Review write operations."""

    @staticmethod
    def create_review(case: Case, reviewer=None, status: str = 'pending'):
        """Create a new review."""
        with transaction.atomic():
            assigned_at = timezone.now() if reviewer else None
            
            review = Review.objects.create(
                case=case,
                reviewer=reviewer,
                status=status,
                assigned_at=assigned_at
            )
            review.full_clean()
            review.save()
            return review

    @staticmethod
    def update_review(review, **fields):
        """Update review fields."""
        with transaction.atomic():
            for key, value in fields.items():
                if hasattr(review, key):
                    setattr(review, key, value)
            review.full_clean()
            review.save()
            return review

    @staticmethod
    def assign_reviewer(review, reviewer):
        """Assign a reviewer to a review."""
        with transaction.atomic():
            review.reviewer = reviewer
            review.status = 'in_progress'
            review.assigned_at = timezone.now()
            review.full_clean()
            review.save()
            return review

    @staticmethod
    def complete_review(review):
        """Mark review as completed."""
        with transaction.atomic():
            review.status = 'completed'
            review.completed_at = timezone.now()
            review.full_clean()
            review.save()
            return review

    @staticmethod
    def cancel_review(review):
        """Cancel a review."""
        with transaction.atomic():
            review.status = 'cancelled'
            review.full_clean()
            review.save()
            return review

    @staticmethod
    def delete_review(review):
        """Delete a review."""
        with transaction.atomic():
            review.delete()

