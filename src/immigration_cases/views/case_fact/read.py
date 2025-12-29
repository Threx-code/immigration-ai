from rest_framework import status
from main_system.base.auth_api import AuthAPI
from immigration_cases.services.case_fact_service import CaseFactService
from immigration_cases.serializers.case_fact.read import CaseFactSerializer, CaseFactListSerializer


class CaseFactListAPI(AuthAPI):
    """Get list of case facts. Supports filtering by case_id."""

    def get(self, request):
        case_id = request.query_params.get('case_id', None)

        if case_id:
            facts = CaseFactService.get_by_case(case_id)
        else:
            facts = CaseFactService.get_all()

        return self.api_response(
            message="Case facts retrieved successfully.",
            data=CaseFactListSerializer(facts, many=True).data,
            status_code=status.HTTP_200_OK
        )


class CaseFactDetailAPI(AuthAPI):
    """Get case fact by ID."""

    def get(self, request, id):
        fact = CaseFactService.get_by_id(id)
        if not fact:
            return self.api_response(
                message=f"Case fact with ID '{id}' not found.",
                data=None,
                status_code=status.HTTP_404_NOT_FOUND
            )

        return self.api_response(
            message="Case fact retrieved successfully.",
            data=CaseFactSerializer(fact).data,
            status_code=status.HTTP_200_OK
        )

