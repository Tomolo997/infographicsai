from .base import *

DEBUG = True
SECRET_KEY = 'django-insecure-j=#8bsh4ywzr_br0-5p84hlm1i6$=2dg(04n=-!00q()%fqp@k'
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'b4124e117e7b.ngrok-free.app', '*.b4124e117e7b.ngrok-free.app']

# Add CORS settings for static files

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'infoai',
        'USER': 'ovsenjak',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': 5433
    },
}


EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI = os.environ.get('GOOGLE_REDIRECT_URI')
GOOGLE_REDIRECT_URI_PUBLIC = os.environ.get('GOOGLE_REDIRECT_URI_PUBLIC')

STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')  # Optional in dev

FRONTEND_URL = 'http://localhost:3000'  # Update this to your actual frontend URL
MAGIC_LINK_EXPIRY_MINUTES = 15

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Static files configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = None

# Ensure static files are served in development
if DEBUG:
    STATICFILES_FINDERS = [
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ]
CORS_ALLOW_ALL_ORIGINS = True  # Only use this in development!
CORS_ALLOW_CREDENTIALS = True
# Explicitly allow these headers (use list, not string)
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Allow all HTTP methods
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Specific origins (redundant with CORS_ALLOW_ALL_ORIGINS=True, but good for clarity)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
# Add this to exempt all /api/* endpoints from CSRF
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

# Development CSRF settings
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = False  # False allows JavaScript access
CSRF_USE_SESSIONS = False  # Store CSRF token in cookie instead of session
CSRF_COOKIE_SECURE = False  # Set to True in production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Override REST_FRAMEWORK settings to disable throttling in development
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1000/day',  # High limit for anonymous users in development
        'user': '10000/day'  # High limit for authenticated users in development
    }
}

SITE_URL = 'http://localhost:8000'