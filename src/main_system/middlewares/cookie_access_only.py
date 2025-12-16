from django.conf import settings
from knox.auth import TokenAuthentication
from .cookies_access.local_cookie_access import LocalCookieAccessTokenAuthentication
from .cookies_access.production_cookie_access import ProductionCookieAccessTokenAuthentication
APP_ENVIRONMENTS = ["local", "dev"]

class CookieAccessOnlyTokenAuthentication(TokenAuthentication):

    def authenticate(self, request):
        if settings.APP_ENV in APP_ENVIRONMENTS:
            return LocalCookieAccessTokenAuthentication().authenticate(request=request)
        return ProductionCookieAccessTokenAuthentication().authenticate(request=request)