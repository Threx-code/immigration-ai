from rest_framework import serializers
from data_ingestion.models.rule_validation_task import RuleValidationTask


class RuleValidationTaskSerializer(serializers.ModelSerializer):
    """Serializer for reading rule validation task data."""
    
    parsed_rule_visa_code = serializers.CharField(source='parsed_rule.visa_code', read_only=True)
    parsed_rule_type = serializers.CharField(source='parsed_rule.rule_type', read_only=True)
    parsed_rule_confidence = serializers.FloatField(source='parsed_rule.confidence_score', read_only=True)
    reviewer_email = serializers.EmailField(source='assigned_to.email', read_only=True)
    reviewer_name = serializers.SerializerMethodField()
    
    class Meta:
        model = RuleValidationTask
        fields = [
            'id',
            'parsed_rule',
            'parsed_rule_visa_code',
            'parsed_rule_type',
            'parsed_rule_confidence',
            'assigned_to',
            'reviewer_email',
            'reviewer_name',
            'status',
            'reviewer_notes',
            'reviewed_at',
            'sla_deadline',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_reviewer_name(self, obj):
        """Get reviewer full name."""
        if obj.assigned_to and hasattr(obj.assigned_to, 'profile'):
            return obj.assigned_to.profile.full_name if obj.assigned_to.profile else ""
        return ""


class RuleValidationTaskListSerializer(serializers.ModelSerializer):
    """Serializer for listing rule validation tasks."""
    
    parsed_rule_visa_code = serializers.CharField(source='parsed_rule.visa_code', read_only=True)
    
    class Meta:
        model = RuleValidationTask
        fields = [
            'id',
            'parsed_rule_visa_code',
            'status',
            'sla_deadline',
            'created_at',
        ]

