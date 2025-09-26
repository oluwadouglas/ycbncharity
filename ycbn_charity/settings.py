# Django settings for ycbn_charity project.
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
# Environment-driven configuration for production safety
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-insecure-secret')
DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() in ('1', 'true', 'yes')
ALLOWED_HOSTS = [h for h in os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',') if h]

# CSRF: trusted origins (HTTPS in production; localhost in dev)
_default_csrf = 'https://ycbn.org,https://www.ycbn.org'
CSRF_TRUSTED_ORIGINS = [o for o in os.getenv('CSRF_TRUSTED_ORIGINS', _default_csrf).split(',') if o]

# Canonical site base for absolute URLs and SEO (ensure https)
SITE_BASE_URL = os.getenv('SITE_BASE_URL', 'https://ycbn.org')
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'charity',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'ycbn_charity.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'charity.context_processors.seo_defaults',
            ],
        },
    },
]
WSGI_APPLICATION = 'ycbn_charity.wsgi.application'
# Database: use DATABASE_URL if provided, else fall back to SQLite for local dev
try:
    import dj_database_url  # type: ignore
    DATABASES = {
        'default': dj_database_url.config(default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
    }
except Exception:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
LANGUAGE_CODE = 'en-ug'
TIME_ZONE = 'Africa/Kampala'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Uganda-friendly formatting
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = ','
DECIMAL_SEPARATOR = '.'
DATE_FORMAT = 'j F Y'            # e.g., 5 July 2025
DATETIME_FORMAT = 'j F Y, H:i'   # 5 July 2025, 14:30
SHORT_DATE_FORMAT = 'd/m/Y'      # 05/07/2025
FIRST_DAY_OF_WEEK = 1            # Monday
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
# Collect static into STATIC_ROOT for production serving (e.g., by Nginx)
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Redirects after auth
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Local development cookie settings (helpful for admin login via proxy)
# These are safe in development; production-secure equivalents are below when DEBUG=False
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Security: Prefer HTTPS in production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST = True
