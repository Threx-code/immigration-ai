import logging
from rest_framework import status
from finance.base.guest_api import GuestAPI
from user_device_session.models import UserDeviceSession
from ..serializers.login import UserLoginSerializer
from otp.helpers.otp_base import OTPBaseHandler
from knox.models import AuthToken

logger = logging.getLogger('django')
OTP_TYPE = 'login'

class UserLoginAPIView(GuestAPI):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')

        UserDeviceSession.objects.revoke_all_for_user(user=user)
        AuthToken.objects.filter(user=user).delete()

        otp_handler = OTPBaseHandler(otp_type=OTP_TYPE)
        otp, endpoint_token = otp_handler.create_otp(user=user)

        user_settings = getattr(user, 'user_settings', None)
        if user_settings and user_settings.two_factor_auth:
            return self.api_response(
                message="Two-factor authentication is enabled. Please verify your identity.",
                data={
                    'email': user.email,
                    '2fa_enabled': True,
                    'endpoint_token': endpoint_token
                },
                status_code=status.HTTP_200_OK
            )

        otp_handler.send_otp_email(user=user, otp=otp)
        return self.api_response(
            message="OTP sent to your email",
            data={
                'email': user.email,
                '2fa_enabled': False,
                'endpoint_token': endpoint_token
            },
            status_code=status.HTTP_200_OK
        )
