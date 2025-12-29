from rest_framework import serializers
from human_reviews.models.review import Review


class ReviewUpdateSerializer(serializers.Serializer):
    """Serializer for updating a review."""
    
    status = serializers.ChoiceField(
        choices=Review.STATUS_CHOICES,
        required=False
    )
    reviewer_id = serializers.UUIDField(required=False, allow_null=True)
    assignment_strategy = serializers.ChoiceField(
        choices=['round_robin', 'workload'],
        required=False,
        default='round_robin'
    )

    def validate_reviewer_id(self, value):
        """Validate reviewer exists, has reviewer role, and is staff or admin."""
        if value:
            from users_access.selectors.user_selector import UserSelector
            try:
                reviewer = UserSelector.get_by_id(value)
                if not reviewer:
                    raise serializers.ValidationError(f"Reviewer with ID '{value}' not found.")
                if reviewer.role != 'reviewer':
                    raise serializers.ValidationError(f"User with ID '{value}' does not have reviewer role.")
                if not (reviewer.is_staff or reviewer.is_superuser):
                    raise serializers.ValidationError(f"User with ID '{value}' is not staff or admin.")
            except Exception as e:
                raise serializers.ValidationError(f"Reviewer with ID '{value}' not found.")
        return value


class ReviewAssignSerializer(serializers.Serializer):
    """Serializer for assigning a reviewer to a review."""
    
    reviewer_id = serializers.UUIDField(required=False, allow_null=True)
    assignment_strategy = serializers.ChoiceField(
        choices=['round_robin', 'workload'],
        required=False,
        default='round_robin'
    )

    def validate_reviewer_id(self, value):
        """Validate reviewer exists, has reviewer role, and is staff or admin."""
        if value:
            from users_access.selectors.user_selector import UserSelector
            try:
                reviewer = UserSelector.get_by_id(value)
                if not reviewer:
                    raise serializers.ValidationError(f"Reviewer with ID '{value}' not found.")
                if reviewer.role != 'reviewer':
                    raise serializers.ValidationError(f"User with ID '{value}' does not have reviewer role.")
                if not (reviewer.is_staff or reviewer.is_superuser):
                    raise serializers.ValidationError(f"User with ID '{value}' is not staff or admin.")
            except Exception as e:
                raise serializers.ValidationError(f"Reviewer with ID '{value}' not found.")
        return value

