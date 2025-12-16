from ..models import OTP


class OTPService:

    def __init__(self):
        self.manager = OTP.objects

    def create(self, user, otp, endpoint_token, otp_type):
        return self.manager.create_otp(user=user, otp=otp, endpoint_token=endpoint_token, otp_type=otp_type)

    def verify_otp(self, otp, endpoint_token):
        return self.manager.verify_otp(otp=otp, endpoint_token=endpoint_token)

    def cleanup_expired_otp(self):
        return self.manager.cleanup_expired_otp()

    def get_last_unverified_otp(self, user):
        return self.manager.get_last_unverified_otp(user=user)

    def endpoint_token(self, endpoint_token):
        return self.manager.endpoint_token(endpoint_token=endpoint_token)

    def get_by_endpoint(self, endpoint_token):
        return self.manager.get_by_endpoint(endpoint_token=endpoint_token)

    def resend_otp(self, otp_model, otp):
        return self.manager.resend_otp(otp_model=otp_model, otp=otp)

    def get_by_endpoint_and_user(self, endpoint_token, user):
        return self.manager.get_by_endpoint_and_user(endpoint_token=endpoint_token, user=user)










