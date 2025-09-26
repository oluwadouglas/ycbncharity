# Production settings for ycbn_charity
# Usage: set DJANGO_SETTINGS_MODULE=ycbn_charity.settings_production

import os
from pathlib import Path
from urllib.parse import urlparse
from .settings import *  # noqa: F401,F403

# Base dir
BASE_DIR = Path(__file__).resolve().parent.parent

# Debug and secret key
DEBUG = False
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", SECRET_KEY)

# Hosts
env_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS", "")
if env_hosts:
    ALLOWED_HOSTS = [h.strip() for h in env_hosts.split(",") if h.strip()]

# Site base URL (for canonical links, absolute images)
SITE_BASE_URL = os.environ.get("SITE_BASE_URL", SITE_BASE_URL)

# CSRF trusted origins (include https scheme)
if ALLOWED_HOSTS:
    CSRF_TRUSTED_ORIGINS = [f"https://{h}" for h in ALLOWED_HOSTS if not h.startswith("*")]

# Security settings (reinforced in production)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", "31536000"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

# Optional: WhiteNoise for static files (works without Nginx for static)
if os.environ.get("USE_WHITENOISE", "false").lower() in {"1", "true", "yes", "on"}:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Database: use DATABASE_URL if provided, else fallback to default
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    # Simple parser for postgres:// or sqlite:/// paths
    parsed = urlparse(DATABASE_URL)
    if parsed.scheme.startswith("postgres"):
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': parsed.path.lstrip('/'),
                'USER': parsed.username,
                'PASSWORD': parsed.password,
                'HOST': parsed.hostname,
                'PORT': str(parsed.port or ''),
                'CONN_MAX_AGE': 60,
            }
        }
    elif parsed.scheme.startswith("sqlite"):
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': parsed.path or (BASE_DIR / 'db.sqlite3'),
            }
        }

# Logging: basic sane defaults
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
    },
}
