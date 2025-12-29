from rest_framework import serializers
from immigration_cases.selectors.case_selector import CaseSelector
from users_access.selectors.user_selector import UserSelector


class ReviewCreateSerializer(serializers.Serializer):
    """Serializer for creating a review."""
    
    case_id = serializers.UUIDField(required=True)
    reviewer_id = serializers.UUIDField(required=False, allow_null=True)
    auto_assign = serializers.BooleanField(required=False, default=True)
    assignment_strategy = serializers.ChoiceField(
        choices=['round_robin', 'workload'],
        required=False,
        default='round_robin'
    )

    def validate_case_id(self, value):
        """Validate case exists."""
        try:
            case = CaseSelector.get_by_id(value)
            if not case:
                raise serializers.ValidationError(f"Case with ID '{value}' not found.")
        except Exception as e:
            raise serializers.ValidationError(f"Case with ID '{value}' not found.")
        return value

    def validate_reviewer_id(self, value):
        """Validate reviewer exists, has reviewer role, and is staff or admin."""
        if value:
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

