from rest_framework import status

from finance.base.auth_api import AuthAPI
from finance.totp_issuer import QRCodeGenerator
from user_settings.serializers.setting_serializer import UserSettingSerializer
from user_settings.services.service import UserSettingsService


class UserSettingsListAPIView(AuthAPI):
    service = UserSettingsService()

    def get(self, request):
        user = request.user
        settings = getattr(user, 'user_settings', None)
        if not settings:
            return self.api_response(
                message="User settings not found.",
                data={},
                status_code=status.HTTP_200_OK
            )

        response = UserSettingSerializer(settings).data

        if settings.two_factor_auth and settings.totp_secret:
            qr_base64 = QRCodeGenerator.generate(secret=settings.totp_secret, user_email=user.email)
            response['qr_code'] = qr_base64

        return self.api_response(
            message="User settings retrieved successfully.",
            data=response,
            status_code=status.HTTP_200_OK
        )