from rest_framework import serializers
from immigration_cases.models.case import Case


class CaseUpdateSerializer(serializers.Serializer):
    """Serializer for updating a case."""
    
    status = serializers.ChoiceField(choices=Case.STATUS_CHOICES, required=False)
    jurisdiction = serializers.ChoiceField(choices=Case.JURISDICTION_CHOICES, required=False)

