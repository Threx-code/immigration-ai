from rest_framework import serializers
from immigration_cases.selectors.case_selector import CaseSelector
from ai_decisions.selectors.eligibility_result_selector import EligibilityResultSelector
from ai_decisions.models.eligibility_result import EligibilityResult
from users_access.selectors.user_selector import UserSelector


class DecisionOverrideCreateSerializer(serializers.Serializer):
    """Serializer for creating a decision override."""
    
    case_id = serializers.UUIDField(required=True)
    original_result_id = serializers.UUIDField(required=True)
    overridden_outcome = serializers.ChoiceField(
        choices=EligibilityResult.OUTCOME_CHOICES,
        required=True
    )
    reason = serializers.CharField(required=True, max_length=2000)
    reviewer_id = serializers.UUIDField(required=False, allow_null=True)
    review_id = serializers.UUIDField(required=False, allow_null=True)

    def validate_case_id(self, value):
        """Validate case exists."""
        try:
            case = CaseSelector.get_by_id(value)
            if not case:
                raise serializers.ValidationError(f"Case with ID '{value}' not found.")
        except Exception as e:
            raise serializers.ValidationError(f"Case with ID '{value}' not found.")
        return value

    def validate_original_result_id(self, value):
        """Validate eligibility result exists."""
        try:
            result = EligibilityResultSelector.get_by_id(value)
            if not result:
                raise serializers.ValidationError(f"Eligibility result with ID '{value}' not found.")
        except Exception as e:
            raise serializers.ValidationError(f"Eligibility result with ID '{value}' not found.")
        return value

    def validate(self, attrs):
        """Validate that original result belongs to the case."""
        case_id = attrs.get('case_id')
        original_result_id = attrs.get('original_result_id')
        
        if case_id and original_result_id:
            try:
                case = CaseSelector.get_by_id(case_id)
                result = EligibilityResultSelector.get_by_id(original_result_id)
                if result.case.id != case.id:
                    raise serializers.ValidationError(
                        "Eligibility result does not belong to the specified case."
                    )
            except Exception as e:
                raise serializers.ValidationError(f"Error validating case and result relationship: {str(e)}")
        
        return attrs

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

    def validate_reason(self, value):
        """Validate reason content."""
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Reason cannot be empty.")
        if len(value) > 2000:
            raise serializers.ValidationError("Reason cannot exceed 2000 characters.")
        return value

