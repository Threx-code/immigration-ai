from rest_framework import serializers
from rules_knowledge.models.visa_type import VisaType
from rules_knowledge.selectors.visa_type_selector import VisaTypeSelector


class VisaTypeCreateSerializer(serializers.Serializer):
    """Serializer for creating a visa type."""
    
    jurisdiction = serializers.ChoiceField(choices=VisaType.JURISDICTION_CHOICES, required=True)
    code = serializers.CharField(required=True, max_length=100)
    name = serializers.CharField(required=True, max_length=255)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    is_active = serializers.BooleanField(required=False, default=True)

    def validate_code(self, value):
        """Validate code is unique for the jurisdiction."""
        value = value.strip().upper()
        # Note: Full validation happens in service layer
        return value

    def validate(self, attrs):
        """Validate code is unique for jurisdiction."""
        jurisdiction = attrs.get('jurisdiction')
        code = attrs.get('code')
        
        if jurisdiction and code:
            try:
                VisaTypeSelector.get_by_code(code, jurisdiction)
                raise serializers.ValidationError(
                    f"Visa type with code '{code}' already exists for jurisdiction '{jurisdiction}'."
                )
            except Exception:
                # DoesNotExist is expected
                pass
        
        return attrs

