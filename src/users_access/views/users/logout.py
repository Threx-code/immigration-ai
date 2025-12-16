import logging
from knox.views import LogoutView as KnoxLogoutView, LogoutAllView as KnoxLogoutAllView
from knox.models import AuthToken
from finance.cookies.manager import CookieManager
from user_device_session.models import UserDeviceSession

logger = logging.getLogger('django')


class BaseLogoutMixin:
    COOKIE_NAMES = ['access_token', 'refresh_token']

    def _revoke_tokens(self, request):
        try:
            UserDeviceSession.objects.revoke_all_for_user(user=request.user)
            AuthToken.objects.filter(user=request.user).delete()
        except Exception as e:
            logger.exception(f"Failed to revoke tokens on logout: {e}")

    def _clear_cookies(self, request, response):
        cookie_mgr = CookieManager(request, response)
        cookie_mgr.expire_all_cookies()


class LogoutViewAPI(BaseLogoutMixin, KnoxLogoutAllView):
    def post(self, request, *args, **kwargs):
        self._revoke_tokens(request)
        response = super().post(request, *args, **kwargs)
        self._clear_cookies(request, response)
        return response


class LogoutAllViewAPI(BaseLogoutMixin, KnoxLogoutAllView):
    def post(self, request, *args, **kwargs):
        self._revoke_tokens(request)
        response = super().post(request, *args, **kwargs)
        self._clear_cookies(request, response)
        return response
