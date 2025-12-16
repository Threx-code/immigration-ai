from rest_framework import status
from finance.base.guest_api import GuestAPI
from otp.services.services import OTPService
from ..serializers.create_user_success import UserSerializer
from ..services.user_service import UserService
from ..serializers.create_user import CreateUserSerializer
from otp.helpers.otp_base import OTPBaseHandler
import logging

logger = logging.getLogger('django')

OTP_TYPE = 'registration'

class UserRegistrationAPI(GuestAPI):
    serializer_class = CreateUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = UserService()

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        first_name = serializer.validated_data.get('first_name')
        last_name = serializer.validated_data.get('last_name')
        user = service.create(email, password, first_name.title(), last_name.title())

        # Generate a unique token for the endpoint
        otp_handler = OTPBaseHandler(otp_type=OTP_TYPE)
        otp, endpoint_token = otp_handler.generate_and_send_otp(user=user)
        otp_service = OTPService()
        otp_service.create(user=user, otp=otp, endpoint_token=endpoint_token, otp_type=OTP_TYPE)

        return self.api_response(
            message="User created successfully. Please check your email for confirmation OTP",
            data={
                'user': UserSerializer(user).data,
                'endpoint_token': endpoint_token
            },
            status_code=status.HTTP_200_OK
        )