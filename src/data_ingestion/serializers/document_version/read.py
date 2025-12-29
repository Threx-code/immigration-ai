from rest_framework import serializers
from data_ingestion.models.document_version import DocumentVersion


class DocumentVersionSerializer(serializers.ModelSerializer):
    """Serializer for reading document version data."""
    
    source_url = serializers.CharField(source='source_document.source_url', read_only=True)
    data_source_name = serializers.CharField(source='source_document.data_source.name', read_only=True)
    
    class Meta:
        model = DocumentVersion
        fields = [
            'id',
            'source_document',
            'source_url',
            'data_source_name',
            'content_hash',
            'raw_text',
            'extracted_at',
            'metadata',
        ]
        read_only_fields = ['id', 'content_hash', 'extracted_at']


class DocumentVersionListSerializer(serializers.ModelSerializer):
    """Serializer for listing document versions."""
    
    source_url = serializers.CharField(source='source_document.source_url', read_only=True)
    
    class Meta:
        model = DocumentVersion
        fields = [
            'id',
            'source_url',
            'content_hash',
            'extracted_at',
        ]

