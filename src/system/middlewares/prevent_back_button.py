from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import logging

logger = logging.getLogger('django')


class PreventBackButtonMiddleware(MiddlewareMixin):
    """
    Prevents browser caching and enforces security headers including
    CSP based on CORS_ALLOWED_ORIGINS.
    """

    def process_response(self, request, response):
        try:
            # Prevent caching for authenticated users
            if request.user.is_authenticated:
                response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
                response.headers["Pragma"] = "no-cache"
                response.headers["Expires"] = "0"

            # Security headers
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-XSS-Protection"] = "1; mode=block"

            # Dynamic CSP based on CORS_ALLOWED_ORIGINS
            cors_origins = getattr(settings, "CORS_ALLOWED_ORIGINS", [])
            # Always include 'self'
            csp_sources = ["'self'"] + cors_origins

            # Convert list to space-separated string
            sources_str = " ".join(csp_sources)

            # Only set if not already set
            if "Content-Security-Policy" not in response.headers:
                response.headers["Content-Security-Policy"] = (
                    f"default-src {sources_str}; "
                    f"style-src {sources_str} 'unsafe-inline'; "
                    f"script-src {sources_str} 'unsafe-inline'; "
                    f"img-src {sources_str} data:; "
                    f"connect-src {sources_str};"
                )

        except Exception as e:
            logger.warning(f"PreventBackButtonMiddleware error: {e}")

        return response
