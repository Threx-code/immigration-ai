from rest_framework import status
from main_system.base.auth_api import AuthAPI
from ai_decisions.services.eligibility_result_service import EligibilityResultService
from ai_decisions.serializers.eligibility_result.create import EligibilityResultCreateSerializer
from ai_decisions.serializers.eligibility_result.read import EligibilityResultSerializer


class EligibilityResultCreateAPI(AuthAPI):
    """Create a new eligibility result. Authenticated users can create results."""

    def post(self, request):
        serializer = EligibilityResultCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = EligibilityResultService.create_eligibility_result(
            case_id=serializer.validated_data.get('case_id'),
            visa_type_id=serializer.validated_data.get('visa_type_id'),
            rule_version_id=serializer.validated_data.get('rule_version_id'),
            outcome=serializer.validated_data.get('outcome'),
            confidence=serializer.validated_data.get('confidence', 0.0),
            reasoning_summary=serializer.validated_data.get('reasoning_summary'),
            missing_facts=serializer.validated_data.get('missing_facts')
        )

        if not result:
            return self.api_response(
                message="Error creating eligibility result.",
                data=None,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        return self.api_response(
            message="Eligibility result created successfully.",
            data=EligibilityResultSerializer(result).data,
            status_code=status.HTTP_201_CREATED
        )

