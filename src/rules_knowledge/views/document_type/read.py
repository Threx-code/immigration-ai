from rest_framework import status
from main_system.base.auth_api import AuthAPI
from rules_knowledge.services.document_type_service import DocumentTypeService
from rules_knowledge.serializers.document_type.read import DocumentTypeSerializer, DocumentTypeListSerializer


class DocumentTypeListAPI(AuthAPI):
    """Get list of document types. Supports filtering by is_active."""

    def get(self, request):
        is_active = request.query_params.get('is_active', None)

        if is_active is not None:
            is_active_bool = is_active.lower() == 'true'
            if is_active_bool:
                document_types = DocumentTypeService.get_active()
            else:
                document_types = DocumentTypeService.get_all()
        else:
            document_types = DocumentTypeService.get_all()

        return self.api_response(
            message="Document types retrieved successfully.",
            data=DocumentTypeListSerializer(document_types, many=True).data,
            status_code=status.HTTP_200_OK
        )


class DocumentTypeDetailAPI(AuthAPI):
    """Get document type by ID."""

    def get(self, request, id):
        document_type = DocumentTypeService.get_by_id(id)
        if not document_type:
            return self.api_response(
                message=f"Document type with ID '{id}' not found.",
                data=None,
                status_code=status.HTTP_404_NOT_FOUND
            )

        return self.api_response(
            message="Document type retrieved successfully.",
            data=DocumentTypeSerializer(document_type).data,
            status_code=status.HTTP_200_OK
        )

