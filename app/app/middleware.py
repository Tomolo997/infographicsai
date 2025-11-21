# app/middleware.py
from django.http import HttpResponse

class CustomCorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Handle preflight (OPTIONS) requests
        if request.method == 'OPTIONS' and request.path.startswith('/static/'):
            response = HttpResponse()
            self._add_cors_headers(response)
            return response

        response = self.get_response(request)
        
        # Add headers to all static file responses
        if request.path.startswith('/static/'):
            self._add_cors_headers(response)
            
            # Set proper content type for fonts
            if request.path.endswith('.woff2'):
                response['Content-Type'] = 'font/woff2'

        return response

    def _add_cors_headers(self, response):
        response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response['Access-Control-Allow-Headers'] = '*'
        response['Access-Control-Max-Age'] = '86400'  # 24 hours
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Expose-Headers'] = '*'
        # Add Vary header to help with caching
        response['Vary'] = 'Origin'

        return response