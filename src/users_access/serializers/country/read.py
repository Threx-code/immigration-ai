from rest_framework import serializers
from users_access.models.country import Country


class CountrySerializer(serializers.ModelSerializer):
    """Serializer for Country model."""
    states_count = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = [
            'id',
            'code',
            'name',
            'has_states',
            'is_jurisdiction',
            'is_active',
            'states_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_states_count(self, obj):
        """Get count of active states/provinces for this country."""
        if hasattr(obj, 'states_provinces'):
            return obj.states_provinces.filter(is_active=True).count()
        return 0


class CountryListSerializer(serializers.ModelSerializer):
    """Simplified serializer for country lists."""
    class Meta:
        model = Country
        fields = ['id', 'code', 'name', 'has_states', 'is_jurisdiction']


class CountrySearchSerializer(serializers.Serializer):
    """Serializer for country search."""
    query = serializers.CharField(required=True, max_length=200)

    def validate_query(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("Search query must be at least 2 characters.")
        return value

