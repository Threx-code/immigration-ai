from rest_framework import serializers
from data_ingestion.models.document_diff import DocumentDiff


class DocumentDiffSerializer(serializers.ModelSerializer):
    """Serializer for reading document diff data."""
    
    old_version_hash = serializers.CharField(source='old_version.content_hash', read_only=True)
    new_version_hash = serializers.CharField(source='new_version.content_hash', read_only=True)
    old_version_url = serializers.CharField(source='old_version.source_document.source_url', read_only=True)
    new_version_url = serializers.CharField(source='new_version.source_document.source_url', read_only=True)
    
    class Meta:
        model = DocumentDiff
        fields = [
            'id',
            'old_version',
            'old_version_hash',
            'old_version_url',
            'new_version',
            'new_version_hash',
            'new_version_url',
            'diff_text',
            'change_type',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class DocumentDiffListSerializer(serializers.ModelSerializer):
    """Serializer for listing document diffs."""
    
    class Meta:
        model = DocumentDiff
        fields = [
            'id',
            'change_type',
            'created_at',
        ]

