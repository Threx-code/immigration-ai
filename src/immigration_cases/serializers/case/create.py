from rest_framework import serializers
from immigration_cases.models.case import Case
from users_access.selectors.user_selector import UserSelector


class CaseCreateSerializer(serializers.Serializer):
    """Serializer for creating a case."""
    
    user_id = serializers.UUIDField(required=True)
    jurisdiction = serializers.ChoiceField(choices=Case.JURISDICTION_CHOICES, required=True)
    status = serializers.ChoiceField(choices=Case.STATUS_CHOICES, required=False, default='draft')

    def validate_user_id(self, value):
        """Validate user exists."""
        try:
            user = UserSelector.get_by_id(value)
            if not user:
                raise serializers.ValidationError(f"User with ID '{value}' not found.")
        except Exception as e:
            raise serializers.ValidationError(f"User with ID '{value}' not found.")
        return value

