from rest_framework import status
from main_system.base.auth_api import AuthAPI
from rules_knowledge.services.visa_rule_version_service import VisaRuleVersionService
from rules_knowledge.serializers.visa_rule_version.read import VisaRuleVersionSerializer, VisaRuleVersionListSerializer


class VisaRuleVersionListAPI(AuthAPI):
    """Get list of visa rule versions. Supports filtering by visa_type_id."""

    def get(self, request):
        visa_type_id = request.query_params.get('visa_type_id', None)

        if visa_type_id:
            rule_versions = VisaRuleVersionService.get_by_visa_type(visa_type_id)
        else:
            rule_versions = VisaRuleVersionService.get_all()

        return self.api_response(
            message="Visa rule versions retrieved successfully.",
            data=VisaRuleVersionListSerializer(rule_versions, many=True).data,
            status_code=status.HTTP_200_OK
        )


class VisaRuleVersionDetailAPI(AuthAPI):
    """Get visa rule version by ID."""

    def get(self, request, id):
        rule_version = VisaRuleVersionService.get_by_id(id)
        if not rule_version:
            return self.api_response(
                message=f"Visa rule version with ID '{id}' not found.",
                data=None,
                status_code=status.HTTP_404_NOT_FOUND
            )

        return self.api_response(
            message="Visa rule version retrieved successfully.",
            data=VisaRuleVersionSerializer(rule_version).data,
            status_code=status.HTTP_200_OK
        )

