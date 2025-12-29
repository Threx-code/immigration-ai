from rest_framework import status
from main_system.base.auth_api import AuthAPI
from ai_decisions.services.eligibility_result_service import EligibilityResultService
from ai_decisions.serializers.eligibility_result.read import EligibilityResultSerializer
from ai_decisions.serializers.eligibility_result.update_delete import EligibilityResultUpdateSerializer


class EligibilityResultUpdateAPI(AuthAPI):
    """Update an eligibility result."""

    def patch(self, request, id):
        serializer = EligibilityResultUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = EligibilityResultService.update_eligibility_result(id, **serializer.validated_data)
        if not result:
            return self.api_response(
                message=f"Eligibility result with ID '{id}' not found.",
                data=None,
                status_code=status.HTTP_404_NOT_FOUND
            )

        return self.api_response(
            message="Eligibility result updated successfully.",
            data=EligibilityResultSerializer(result).data,
            status_code=status.HTTP_200_OK
        )


class EligibilityResultDeleteAPI(AuthAPI):
    """Delete an eligibility result."""

    def delete(self, request, id):
        success = EligibilityResultService.delete_eligibility_result(id)
        if not success:
            return self.api_response(
                message=f"Eligibility result with ID '{id}' not found.",
                data=None,
                status_code=status.HTTP_404_NOT_FOUND
            )

        return self.api_response(
            message="Eligibility result deleted successfully.",
            data=None,
            status_code=status.HTTP_200_OK
        )

