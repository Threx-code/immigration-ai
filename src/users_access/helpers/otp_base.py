from django.utils.crypto import get_random_string
from ..services.services import OTPService
from ..tasks import send_otp_email
from helpers.generate_hash import GenerateHash


class OTPBaseHandler:
    """A reusable helper for generating and managing OTP workflows."""

    def __init__(self, otp_type: str):
        self.otp_type = otp_type
        self.otp_service = OTPService()

    def generate_endpoint_token(self, user) -> str:
        """Generate a unique token for the endpoint."""
        return GenerateHash.generate_token(user=user)

    def generate_otp(self, length: int = 6) -> str:
        """Generate a random numeric OTP."""
        return get_random_string(length=length, allowed_chars='0123456789')

    def create_otp(self, user):
        """Create and store an OTP for the user."""
        endpoint_token = self.generate_endpoint_token(user=user)
        otp = self.generate_otp()
        self.otp_service.create(user=user, otp=otp, endpoint_token=endpoint_token, otp_type=self.otp_type)
        return otp, endpoint_token


    def send_otp_email(self, user, otp: str):
        """Send the OTP to the user's email asynchronously."""
        send_otp_email.delay(user.email, user.first_name, otp)


    def generate_and_send_otp(self, user):
        """Generate an OTP, store it, and send it via email."""
        otp, endpoint_token = self.create_otp(user=user)
        self.send_otp_email(user=user, otp=otp)
        return otp, endpoint_token