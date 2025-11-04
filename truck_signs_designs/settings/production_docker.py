import environ
from .base import *

DEBUG = False

env = environ.Env()
# reading env file
environ.Env.read_env()

SECRET_KEY = env("DOCKER_SECRET_KEY")

# Update ALLOWED_HOSTS for production
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')

CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DOCKER_DB_NAME'),
        'USER': env('DOCKER_DB_USER'),
        'PASSWORD': env('DOCKER_DB_PASSWORD'),
        'HOST': env('DOCKER_DB_HOST'),
        'PORT': env('DOCKER_DB_PORT'),
        'CONN_MAX_AGE': 600,  # Keep connections open for 10 minutes (connection pooling)
        'OPTIONS': {
            'connect_timeout': 10,  # 10 second connection timeout
            'options': '-c statement_timeout=30000'  # 30 second query timeout
        },
    }
}

STRIPE_PUBLISHABLE_KEY = env("DOCKER_STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = env("DOCKER_STRIPE_SECRET_KEY")

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = env("DOCKER_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("DOCKER_EMAIL_HOST_PASSWORD")

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = '/app/static'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = '/app/media'

# Whitenoise configuration
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
] + MIDDLEWARE

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Whitenoise settings
WHITENOISE_USE_FINDERS = False  # Disable for better performance - use collected static files
WHITENOISE_AUTOREFRESH = False  # Disable auto-refresh - requires server restart for changes

# Django REST Framework browsable API settings
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
