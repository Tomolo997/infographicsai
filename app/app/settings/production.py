from .base import *
import os

DEBUG = os.environ.get('DEBUG', 'False') == 'True'
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')

DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.postgresql',
        'NAME':  os.environ.get('DB_NAME'),
        'USER':  os.environ.get('DB_USER'),
        'PASSWORD':  os.environ.get('DB_PASSWORD'),  # Replace with your actual password
        'HOST':  os.environ.get('DB_HOST'),
        'PORT':  os.environ.get('DB_PORT'),  # Or '5432' if you didn't change the default port
        'OPTIONS': {
            'sslmode': 'require',  # Enforce SSL connection
        },
    }
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

# Add production-specific security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

FRONTEND_URL = 'https://ainfographic.com'  # Update this to your actual frontend URL
MAGIC_LINK_EXPIRY_MINUTES = 15

CORS_ALLOWED_ORIGINS = [
    "https://ainfographic.com",
    # Add other production domains as needed
]

# In production, you might want to be more restrictive with exposed headers
CORS_EXPOSE_HEADERS = [
    'access-control-allow-origin',
    'access-control-allow-credentials',
]


# Force HTTPS in production
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')