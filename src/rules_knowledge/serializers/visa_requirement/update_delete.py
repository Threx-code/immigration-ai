from rest_framework import serializers


class VisaRequirementUpdateSerializer(serializers.Serializer):
    """Serializer for updating a visa requirement."""
    
    description = serializers.CharField(required=False)
    condition_expression = serializers.JSONField(required=False)
    is_active = serializers.BooleanField(required=False)

