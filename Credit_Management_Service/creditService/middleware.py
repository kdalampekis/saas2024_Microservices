# creditService/middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class CsrfExemptMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if hasattr(settings, 'CSRF_EXEMPT_PATHS') and request.path in settings.CSRF_EXEMPT_PATHS:
            setattr(request, '_dont_enforce_csrf_checks', True)
