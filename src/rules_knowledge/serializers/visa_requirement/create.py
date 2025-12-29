from rest_framework import serializers
from rules_knowledge.selectors.visa_rule_version_selector import VisaRuleVersionSelector


class VisaRequirementCreateSerializer(serializers.Serializer):
    """Serializer for creating a visa requirement."""
    
    rule_version_id = serializers.UUIDField(required=True)
    requirement_code = serializers.CharField(required=True, max_length=100)
    description = serializers.CharField(required=True)
    condition_expression = serializers.JSONField(required=True)
    is_active = serializers.BooleanField(required=False, default=True)

    def validate_rule_version_id(self, value):
        """Validate rule version exists."""
        try:
            rule_version = VisaRuleVersionSelector.get_by_id(value)
            if not rule_version:
                raise serializers.ValidationError(f"Rule version with ID '{value}' not found.")
        except Exception as e:
            raise serializers.ValidationError(f"Rule version with ID '{value}' not found.")
        return value

    def validate_requirement_code(self, value):
        """Validate requirement code."""
        value = value.strip().upper()
        if not value:
            raise serializers.ValidationError("Requirement code cannot be empty.")
        return value

