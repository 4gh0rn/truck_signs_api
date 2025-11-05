import environ
from .base import *

DEBUG = False

env = environ.Env()
# reading env file - suppress warning if .env doesn't exist (vars come from Docker Compose)
# Check if .env file exists in project root before reading
env_file = os.path.join(ROOT_BASE_DIR, '.env')
if os.path.exists(env_file):
    environ.Env.read_env(env_file)

SECRET_KEY = env("DOCKER_SECRET_KEY")

# Update ALLOWED_HOSTS for production
# Use django-environ's list() method with default fallback
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])
# Filter out empty strings just in case
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS if host.strip()]

# CORS_ALLOWED_ORIGINS can be empty (no CORS allowed) or contain valid origins
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])
# Filter out empty strings to avoid validation errors
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in CORS_ALLOWED_ORIGINS if origin.strip()]

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
