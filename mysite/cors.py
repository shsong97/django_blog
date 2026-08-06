from django import http
from django.utils.deprecation import MiddlewareMixin

try:
    from django.conf import settings

    XS_SHARING_ALLOWED_ORIGINS = getattr(settings, 'XS_SHARING_ALLOWED_ORIGINS', '*')
    XS_SHARING_ALLOWED_METHODS = getattr(
        settings,
        'XS_SHARING_ALLOWED_METHODS',
        ['POST', 'GET', 'OPTIONS', 'PUT', 'DELETE'],
    )
except Exception:
    XS_SHARING_ALLOWED_ORIGINS = '*'
    XS_SHARING_ALLOWED_METHODS = ['POST', 'GET', 'OPTIONS', 'PUT', 'DELETE']

XS_SHARING_ALLOW_CREDENTIALS = True


class XsSharingMiddleware(MiddlewareMixin):
    """
    Allow cross-domain XHR using CORS headers.
    """

    def process_request(self, request):
        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin'] = XS_SHARING_ALLOWED_ORIGINS
            response['Access-Control-Allow-Methods'] = ','.join(XS_SHARING_ALLOWED_METHODS)
            response['Access-Control-Allow-Credentials'] = str(XS_SHARING_ALLOW_CREDENTIALS).lower()
            response['Access-Control-Allow-Headers'] = 'authorization'
            return response
        return None

    def process_response(self, request, response):
        if response.has_header('Access-Control-Allow-Origin'):
            return response

        response['Access-Control-Allow-Origin'] = XS_SHARING_ALLOWED_ORIGINS
        response['Access-Control-Allow-Methods'] = ','.join(XS_SHARING_ALLOWED_METHODS)
        response['Access-Control-Allow-Credentials'] = str(XS_SHARING_ALLOW_CREDENTIALS).lower()
        response['Access-Control-Allow-Headers'] = 'authorization'
        return response
