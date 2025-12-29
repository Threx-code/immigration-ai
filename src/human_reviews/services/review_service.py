import logging
from typing import Optional
from django.utils import timezone
from human_reviews.models.review import Review
from human_reviews.repositories.review_repository import ReviewRepository
from human_reviews.selectors.review_selector import ReviewSelector
from immigration_cases.selectors.case_selector import CaseSelector
from users_access.selectors.user_selector import UserSelector
from users_access.services.user_service import UserService

logger = logging.getLogger('django')


class ReviewService:
    """Service for Review business logic."""

    @staticmethod
    def create_review(case_id: str, reviewer_id: str = None, auto_assign: bool = True,
                     assignment_strategy: str = 'round_robin'):
        """
        Create a new review.
        
        Args:
            case_id: Case ID
            reviewer_id: Optional reviewer ID (if provided, auto_assign is ignored)
            auto_assign: Whether to automatically assign a reviewer
            assignment_strategy: 'round_robin' or 'workload'
        """
        try:
            case = CaseSelector.get_by_id(case_id)
            
            reviewer = None
            if reviewer_id:
                reviewer = UserSelector.get_by_id(reviewer_id)
                # Verify reviewer has reviewer role AND is staff or admin
                if reviewer.role != 'reviewer':
                    logger.error(f"User {reviewer_id} does not have reviewer role")
                    return None
                if not (reviewer.is_staff or reviewer.is_superuser):
                    logger.error(f"User {reviewer_id} is not staff or admin")
                    return None
            elif auto_assign:
                # Auto-assign reviewer based on strategy
                if assignment_strategy == 'workload':
                    reviewer = UserSelector.get_reviewer_by_workload()
                else:
                    reviewer = UserSelector.get_reviewer_round_robin()
                
                if reviewer:
                    # Update last_assigned_at for round-robin tracking
                    UserService.update_user_last_assigned_at(reviewer)
            
            review = ReviewRepository.create_review(case=case, reviewer=reviewer)
            return review
        except Exception as e:
            logger.error(f"Error creating review: {e}")
            return None

    @staticmethod
    def get_all():
        """Get all reviews."""
        try:
            return ReviewSelector.get_all()
        except Exception as e:
            logger.error(f"Error fetching all reviews: {e}")
            return Review.objects.none()

    @staticmethod
    def get_by_case(case_id: str):
        """Get reviews by case."""
        try:
            case = CaseSelector.get_by_id(case_id)
            return ReviewSelector.get_by_case(case)
        except Exception as e:
            logger.error(f"Error fetching reviews for case {case_id}: {e}")
            return Review.objects.none()

    @staticmethod
    def get_by_status(status: str):
        """Get reviews by status."""
        try:
            return ReviewSelector.get_by_status(status)
        except Exception as e:
            logger.error(f"Error fetching reviews by status {status}: {e}")
            return Review.objects.none()

    @staticmethod
    def get_by_reviewer(reviewer_id: str):
        """Get reviews by reviewer."""
        try:
            reviewer = UserSelector.get_by_id(reviewer_id)
            return ReviewSelector.get_by_reviewer(reviewer)
        except Exception as e:
            logger.error(f"Error fetching reviews for reviewer {reviewer_id}: {e}")
            return Review.objects.none()

    @staticmethod
    def get_pending_by_reviewer(reviewer_id: str):
        """Get pending/in_progress reviews by reviewer."""
        try:
            reviewer = UserSelector.get_by_id(reviewer_id)
            return ReviewSelector.get_pending_by_reviewer(reviewer)
        except Exception as e:
            logger.error(f"Error fetching pending reviews for reviewer {reviewer_id}: {e}")
            return Review.objects.none()

    @staticmethod
    def get_pending():
        """Get all pending reviews (not assigned)."""
        try:
            return ReviewSelector.get_pending()
        except Exception as e:
            logger.error(f"Error fetching pending reviews: {e}")
            return Review.objects.none()

    @staticmethod
    def get_by_id(review_id: str) -> Optional[Review]:
        """Get review by ID."""
        try:
            return ReviewSelector.get_by_id(review_id)
        except Review.DoesNotExist:
            logger.error(f"Review {review_id} not found")
            return None
        except Exception as e:
            logger.error(f"Error fetching review {review_id}: {e}")
            return None

    @staticmethod
    def assign_reviewer(review_id: str, reviewer_id: str, assignment_strategy: str = 'round_robin') -> Optional[Review]:
        """Assign a reviewer to a review."""
        try:
            review = ReviewSelector.get_by_id(review_id)
            
            if reviewer_id:
                reviewer = UserSelector.get_by_id(reviewer_id)
                # Verify reviewer has reviewer role AND is staff or admin
                if reviewer.role != 'reviewer':
                    logger.error(f"User {reviewer_id} does not have reviewer role")
                    return None
                if not (reviewer.is_staff or reviewer.is_superuser):
                    logger.error(f"User {reviewer_id} is not staff or admin")
                    return None
            else:
                # Auto-assign based on strategy
                if assignment_strategy == 'workload':
                    reviewer = UserSelector.get_reviewer_by_workload()
                else:
                    reviewer = UserSelector.get_reviewer_round_robin()
                
                if not reviewer:
                    logger.error("No available reviewers found")
                    return None
                
                # Update last_assigned_at for round-robin tracking
                UserService.update_user_last_assigned_at(reviewer)
            
            return ReviewRepository.assign_reviewer(review, reviewer)
        except Review.DoesNotExist:
            logger.error(f"Review {review_id} not found")
            return None
        except Exception as e:
            logger.error(f"Error assigning reviewer to review {review_id}: {e}")
            return None

    @staticmethod
    def complete_review(review_id: str) -> Optional[Review]:
        """Complete a review."""
        try:
            review = ReviewSelector.get_by_id(review_id)
            return ReviewRepository.complete_review(review)
        except Review.DoesNotExist:
            logger.error(f"Review {review_id} not found")
            return None
        except Exception as e:
            logger.error(f"Error completing review {review_id}: {e}")
            return None

    @staticmethod
    def cancel_review(review_id: str) -> Optional[Review]:
        """Cancel a review."""
        try:
            review = ReviewSelector.get_by_id(review_id)
            return ReviewRepository.cancel_review(review)
        except Review.DoesNotExist:
            logger.error(f"Review {review_id} not found")
            return None
        except Exception as e:
            logger.error(f"Error cancelling review {review_id}: {e}")
            return None

    @staticmethod
    def update_review(review_id: str, **fields) -> Optional[Review]:
        """Update review fields."""
        try:
            review = ReviewSelector.get_by_id(review_id)
            return ReviewRepository.update_review(review, **fields)
        except Review.DoesNotExist:
            logger.error(f"Review {review_id} not found")
            return None
        except Exception as e:
            logger.error(f"Error updating review {review_id}: {e}")
            return None

    @staticmethod
    def delete_review(review_id: str) -> bool:
        """Delete a review."""
        try:
            review = ReviewSelector.get_by_id(review_id)
            ReviewRepository.delete_review(review)
            return True
        except Review.DoesNotExist:
            logger.error(f"Review {review_id} not found")
            return False
        except Exception as e:
            logger.error(f"Error deleting review {review_id}: {e}")
            return False

