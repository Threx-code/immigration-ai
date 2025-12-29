from rest_framework import status
from main_system.base.auth_api import AuthAPI
from main_system.permissions.is_admin_or_staff import IsAdminOrStaff
from compliance.services.audit_log_service import AuditLogService
from compliance.serializers.audit_log.read import (
    AuditLogSerializer,
    AuditLogListSerializer
)


class AuditLogListAPI(AuthAPI):
    """Get all audit logs."""
    permission_classes = [IsAdminOrStaff]

    def get(self, request):
        level = request.query_params.get('level', None)
        logger_name = request.query_params.get('logger_name', None)
        limit = request.query_params.get('limit', 100)
        
        try:
            limit = int(limit)
        except (ValueError, TypeError):
            limit = 100
        
        if level:
            audit_logs = AuditLogService.get_by_level(level)
        elif logger_name:
            audit_logs = AuditLogService.get_by_logger_name(logger_name)
        else:
            audit_logs = AuditLogService.get_recent(limit)

        return self.api_response(
            message="Audit logs retrieved successfully.",
            data=AuditLogListSerializer(audit_logs, many=True).data,
            status_code=status.HTTP_200_OK
        )


class AuditLogDetailAPI(AuthAPI):
    """Get audit log by ID."""
    permission_classes = [IsAdminOrStaff]

    def get(self, request, id):
        audit_log = AuditLogService.get_by_id(id)
        
        if not audit_log:
            return self.api_response(
                message=f"Audit log with ID '{id}' not found.",
                data=None,
                status_code=status.HTTP_404_NOT_FOUND
            )

        return self.api_response(
            message="Audit log retrieved successfully.",
            data=AuditLogSerializer(audit_log).data,
            status_code=status.HTTP_200_OK
        )

