from django.db import models, transaction
import logging
from django.utils import timezone

logger = logging.getLogger('django')


class OTPManager(models.Manager):

    def create_otp(self, user, otp, endpoint_token, otp_type):
        try:
            with transaction.atomic():
                expires_at = timezone.now() + timezone.timedelta(minutes=10)

                otp_data = self.create(
                    user=user,
                    otp=otp,
                    endpoint_token=endpoint_token,
                    type=otp_type,
                    expires_at=expires_at
                )
                logger.info(f"OTP created for user {user.email} with OTP {otp}")
                otp_data.full_clean()
                return otp_data
        except Exception as e:
            logger.error(f"Error creating OTP: {e}")
            return None

    def resend_otp(self, otp_model, otp):
        try:
            with transaction.atomic():
                expires_at = timezone.now() + timezone.timedelta(minutes=10)
                otp_model.otp = otp
                otp_model.expires_at = expires_at
                otp_model.is_verified = False
                otp_model.save()
                logger.info(f"OTP resent for user {otp_model.user.email} with new OTP {otp}")

                otp_model.full_clean()
                return otp_model
        except Exception as e:
            logger.error(f"Error resending OTP: {e}")
            return None

    def verify_otp(self, otp, endpoint_token):
        try:
            otp_data = self.filter(
                otp=otp,
                endpoint_token=endpoint_token,
                is_verified=False,
                expires_at__gt=timezone.now()
            ).last()

            if otp_data:
                otp_data.is_verified = True
                otp_data.save()
                user = otp_data.user
                logger.info(f"OTP verified for user {user.email}")
                return user
            else:
                logger.warning(f"OTP verification failed for endpoint token {endpoint_token} with OTP {otp}")
            return False
        except Exception as e:
            logger.error(f"Error verifying OTP: {e}")
            return False

    def cleanup_expired_otp(self):
        try:
            expired_otps = self.filter(
                expires_at__lt=timezone.now(),
                is_verified=False
            )
            count = expired_otps.count()
            expired_otps.delete()
            logger.info(f"Deleted {count} expired OTPs")
        except Exception as e:
            logger.error(f"Error cleaning up expired OTPs: {e}")
            return False

    def endpoint_token(self, endpoint_token):
        try:
            endpoint = self.filter(
                endpoint_token=endpoint_token,
                is_verified=False,
                expires_at__gt=timezone.now()
            ).last()
            if not endpoint:
                logger.warning(f"No unverified OTP found for endpoint token {endpoint_token}")
                return None
            logger.info(f"Endpoint token fetched: {endpoint_token}")
            return endpoint
        except Exception as e:
            logger.error(f"Error fetching endpoint token: {e}")
            return None

    def get_by_endpoint(self, endpoint_token):
        try:
            endpoint = self.filter(
                endpoint_token=endpoint_token,
                is_verified=False
            ).last()
            if not endpoint:
                logger.warning(f"No unverified OTP found for endpoint token {endpoint_token}")
                return None
            logger.info(f"Endpoint token fetched: {endpoint_token}")
            return endpoint
        except Exception as e:
            logger.error(f"Error fetching endpoint token: {e}")
            return None


    def get_by_endpoint_and_user(self, endpoint_token, user):
        try:
            endpoint = self.filter(
                endpoint_token=endpoint_token,
                user=user
            ).last()
            if not endpoint:
                logger.warning(f"Wrong user{user}, or wrong endpoint_token: {endpoint_token}")
                return None
            logger.info(f"Endpoint token fetched: {endpoint_token}")
            return endpoint
        except Exception as e:
            logger.error(f"Error fetching endpoint token: {e}")
            return None

    def get_last_unverified_otp(self, user):
        try:
            otp = self.filter(
                user=user,
                is_verified=False,
                expires_at__gt=timezone.now()
            ).last()

            if not otp:
                logger.warning(f"No unverified OTP found for user {user.email}")
                return None
            logger.info(f"Last unverified OTP fetched for user {user.email}")
            return otp
        except Exception as e:
            logger.error(f"Error fetching last unverified OTP: {e}")
            return None




