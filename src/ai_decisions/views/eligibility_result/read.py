from rest_framework import status
from main_system.base.auth_api import AuthAPI
from ai_decisions.services.eligibility_result_service import EligibilityResultService
from ai_decisions.serializers.eligibility_result.read import EligibilityResultSerializer, EligibilityResultListSerializer


class EligibilityResultListAPI(AuthAPI):
    """Get list of eligibility results. Supports filtering by case_id."""

    def get(self, request):
        case_id = request.query_params.get('case_id', None)

        if case_id:
            results = EligibilityResultService.get_by_case(case_id)
        else:
            results = EligibilityResultService.get_all()

        return self.api_response(
            message="Eligibility results retrieved successfully.",
            data=EligibilityResultListSerializer(results, many=True).data,
            status_code=status.HTTP_200_OK
        )


class EligibilityResultDetailAPI(AuthAPI):
    """Get eligibility result by ID."""

    def get(self, request, id):
        result = EligibilityResultService.get_by_id(id)
        if not result:
            return self.api_response(
                message=f"Eligibility result with ID '{id}' not found.",
                data=None,
                status_code=status.HTTP_404_NOT_FOUND
            )

        return self.api_response(
            message="Eligibility result retrieved successfully.",
            data=EligibilityResultSerializer(result).data,
            status_code=status.HTTP_200_OK
        )

