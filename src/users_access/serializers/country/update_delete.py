from rest_framework import serializers
from users_access.selectors.country_selector import CountrySelector
from users_access.models.country import Country


class CountryUpdateSerializer(serializers.Serializer):
    """Serializer for updating a country."""
    name = serializers.CharField(required=False, max_length=200)
    has_states = serializers.BooleanField(required=False)
    is_jurisdiction = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(required=False)

    def validate_name(self, value):
        if value is not None:
            value = value.strip()
            if not value:
                raise serializers.ValidationError("Country name cannot be empty.")
            if len(value) < 2:
                raise serializers.ValidationError("Country name must be at least 2 characters.")
        return value


class CountryDeleteSerializer(serializers.Serializer):
    """Serializer for validating country deletion."""
    id = serializers.UUIDField(required=True)

    def validate_id(self, value):
        try:
            CountrySelector.get_by_id(value)
        except Country.DoesNotExist:
            raise serializers.ValidationError(f"Country with ID '{value}' not found.")
        return value

