from django.conf import settings
from django.utils import timezone
from knox.auth import TokenAuthentication
from users_access.models.user_device_session import UserDeviceSession
from main_system.cookies.manager import CookieManager
import logging

logger = logging.getLogger('django')

ACCESS_COOKIE_NAME = getattr(settings, "ACCESS_COOKIE_NAME", "access_token")
SESSION_COOKIE_NAME = getattr(settings, "SESSION_COOKIE_NAME", "sessionid")
FINGERPRINT_COOKIE_NAME = getattr(settings, "FINGERPRINT_COOKIE_NAME", "fingerprint")
MFA_VERIFIED_COOKIE_NAME = getattr(settings, "MFA_VERIFIED_COOKIE_NAME", "mfa_verified")

REQUEST_METHODS = ["POST", "PUT", "PATCH", "DELETE"]

class ProductionDeviceSessionRefreshMiddleware:

    def process_request(self, request):
        cookie_mgr = CookieManager(request, None)

        access_token = cookie_mgr.get_cookie(key=ACCESS_COOKIE_NAME, sign=False)
        if access_token and "HTTP_AUTHORIZATION" not in request.META:
            request.META["HTTP_AUTHORIZATION"] = f"Token {access_token}"

        return None

    def process_response(self, request, response):
        cookie_mgr = CookieManager(request, response)

        session_id = cookie_mgr.get_cookie(key=SESSION_COOKIE_NAME, sign=False)
        access_token = cookie_mgr.get_cookie(key=ACCESS_COOKIE_NAME, sign=False)
        fingerprint = cookie_mgr.get_cookie(key=FINGERPRINT_COOKIE_NAME)
        mfa_verified = cookie_mgr.get_cookie(key=MFA_VERIFIED_COOKIE_NAME)

        # If missing, expire cookies
        if not session_id or not access_token or not fingerprint:
            return response

        device_session = UserDeviceSession.objects.get_by_session_id(session_id, fingerprint)
        if not device_session or device_session.revoked:
            cookie_mgr.expire_cookies_and_tokens(token_obj=access_token, device_session=device_session)
            return response

        try:
            auth = TokenAuthentication()
            user, token_obj = auth.authenticate_credentials(access_token.encode())
            if user.id != device_session.user_id:
                cookie_mgr.expire_cookies_and_tokens(token_obj=access_token, device_session=device_session)
                return response
            if not user.is_active:
                cookie_mgr.expire_cookies_and_tokens(token_obj=access_token, device_session=device_session)
                return response
            if not token_obj:
                cookie_mgr.expire_cookies_and_tokens(token_obj=access_token, device_session=device_session)
                return response
            if token_obj.expiry and token_obj.expiry < timezone.now():
                cookie_mgr.expire_cookies_and_tokens(token_obj=access_token, device_session=device_session)
                return response
        except Exception as e:
            logger.warning(f"Access token invalid or expired: {e}")
            cookie_mgr.expire_cookies_and_tokens(token_obj=access_token, device_session=device_session)
            return response

        # Validate fingerprint
        if fingerprint != device_session.fingerprint:
            logger.warning(f"Fingerprint mismatch for user {device_session.user_id}")
            cookie_mgr.expire_cookies_and_tokens(token_obj=access_token, device_session=device_session)
            return response

        # Mark device session active
        UserDeviceSession.objects.mark_active(session_id)

        # Refresh MFA verified cookie if valid
        if mfa_verified == "true":
            cookie_mgr.set_mfa_verified()

        return response
