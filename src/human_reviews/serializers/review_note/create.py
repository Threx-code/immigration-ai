from rest_framework import serializers
from human_reviews.selectors.review_selector import ReviewSelector


class ReviewNoteCreateSerializer(serializers.Serializer):
    """Serializer for creating a review note."""
    
    review_id = serializers.UUIDField(required=True)
    note = serializers.CharField(required=True, max_length=5000)
    is_internal = serializers.BooleanField(required=False, default=False)

    def validate_review_id(self, value):
        """Validate review exists."""
        try:
            review = ReviewSelector.get_by_id(value)
            if not review:
                raise serializers.ValidationError(f"Review with ID '{value}' not found.")
        except Exception as e:
            raise serializers.ValidationError(f"Review with ID '{value}' not found.")
        return value

    def validate_note(self, value):
        """Validate note content."""
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Note cannot be empty.")
        if len(value) > 5000:
            raise serializers.ValidationError("Note cannot exceed 5000 characters.")
        return value

