from rest_framework import serializers


class ReviewNoteUpdateSerializer(serializers.Serializer):
    """Serializer for updating a review note."""
    
    note = serializers.CharField(required=False, max_length=5000)
    is_internal = serializers.BooleanField(required=False)

    def validate_note(self, value):
        """Validate note content."""
        if value is not None:
            value = value.strip()
            if not value:
                raise serializers.ValidationError("Note cannot be empty.")
            if len(value) > 5000:
                raise serializers.ValidationError("Note cannot exceed 5000 characters.")
        return value

