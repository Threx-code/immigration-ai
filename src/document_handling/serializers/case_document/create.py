from rest_framework import serializers
from document_handling.selectors.case_document_selector import CaseDocumentSelector
from rules_knowledge.selectors.document_type_selector import DocumentTypeSelector


class CaseDocumentCreateSerializer(serializers.Serializer):
    """Serializer for creating a case document with file upload."""
    
    case_id = serializers.UUIDField(required=True)
    document_type_id = serializers.UUIDField(required=True)
    file = serializers.FileField(required=True, allow_empty_file=False)
    
    # Optional fields (can be auto-detected from file)
    file_name = serializers.CharField(required=False, max_length=255, allow_blank=True)
    file_size = serializers.IntegerField(required=False, allow_null=True, min_value=0)
    mime_type = serializers.CharField(required=False, max_length=100, allow_null=True, allow_blank=True)

    def validate_case_id(self, value):
        """Validate case exists."""
        try:
            from immigration_cases.models.case import Case
            case = Case.objects.get(id=value)
            if not case:
                raise serializers.ValidationError(f"Case with ID '{value}' not found.")
        except Case.DoesNotExist:
            raise serializers.ValidationError(f"Case with ID '{value}' not found.")
        except Exception as e:
            raise serializers.ValidationError(f"Error validating case: {str(e)}")
        return value

    def validate_document_type_id(self, value):
        """Validate document type exists."""
        try:
            document_type = DocumentTypeSelector.get_by_id(value)
            if not document_type or not document_type.is_active:
                raise serializers.ValidationError(f"Document type with ID '{value}' not found or inactive.")
        except Exception as e:
            raise serializers.ValidationError(f"Document type with ID '{value}' not found.")
        return value

    def validate(self, attrs):
        """Validate file and extract metadata."""
        file = attrs.get('file')
        if not file:
            raise serializers.ValidationError({"file": "File is required."})
        
        # Auto-detect file metadata if not provided
        if not attrs.get('file_name'):
            attrs['file_name'] = file.name
        
        if not attrs.get('file_size'):
            attrs['file_size'] = file.size
        
        if not attrs.get('mime_type') and hasattr(file, 'content_type'):
            attrs['mime_type'] = file.content_type
        
        # Validate file using FileStorageService
        from document_handling.services.file_storage_service import FileStorageService
        is_valid, error = FileStorageService.validate_file(file)
        if not is_valid:
            raise serializers.ValidationError({"file": error})
        
        return attrs

