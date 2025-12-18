from rest_framework import serializers
from users_access.selectors.country_selector import CountrySelector


class CountryCreateSerializer(serializers.Serializer):
    """Serializer for creating a country."""
    code = serializers.CharField(required=True, max_length=2, min_length=2)
    name = serializers.CharField(required=True, max_length=200)
    has_states = serializers.BooleanField(required=False, default=False)
    is_jurisdiction = serializers.BooleanField(required=False, default=False)
    is_active = serializers.BooleanField(required=False, default=True)

    def validate_code(self, value):
        value = value.strip().upper()
        if len(value) != 2:
            raise serializers.ValidationError("Country code must be exactly 2 characters (ISO 3166-1 alpha-2).")
        if CountrySelector.code_exists(value):
            raise serializers.ValidationError(f"Country with code '{value}' already exists.")
        return value

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Country name cannot be empty.")
        if len(value) < 2:
            raise serializers.ValidationError("Country name must be at least 2 characters.")
        return value

