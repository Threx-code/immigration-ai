from django.db import transaction
from human_reviews.models.review_note import ReviewNote
from human_reviews.models.review import Review


class ReviewNoteRepository:
    """Repository for ReviewNote write operations."""

    @staticmethod
    def create_review_note(review: Review, note: str, is_internal: bool = False):
        """Create a new review note."""
        with transaction.atomic():
            review_note = ReviewNote.objects.create(
                review=review,
                note=note,
                is_internal=is_internal
            )
            review_note.full_clean()
            review_note.save()
            return review_note

    @staticmethod
    def update_review_note(review_note, **fields):
        """Update review note fields."""
        with transaction.atomic():
            for key, value in fields.items():
                if hasattr(review_note, key):
                    setattr(review_note, key, value)
            review_note.full_clean()
            review_note.save()
            return review_note

    @staticmethod
    def delete_review_note(review_note):
        """Delete a review note."""
        with transaction.atomic():
            review_note.delete()

