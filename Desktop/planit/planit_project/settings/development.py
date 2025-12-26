"""
Development settings for planit_project.
"""

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%or=3m-gp%c^9+26l71-i6^(r#&#5s*x7%wdf!^n)1swk$&l8$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1',
    'testserver',     # Django 테스트용
    '10.185.16.201',  # 현재 컴퓨터의 IP 주소
    '10.185.*',       # 로컬 네트워크 범위
    '192.168.*',      # 일반적인 로컬 네트워크 범위
    '172.16.*',       # 사설 IP 범위
    'planit.boramae.club',
    'www.planit.boramae.club',
    '35.163.12.109',
    '*.amazonaws.com',
    '*.compute.amazonaws.com',
]

# CSRF settings for development
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://127.0.0.1:50616',  # Browser preview URL
    'http://127.0.0.1:50617',  # Additional browser preview ports
    'http://127.0.0.1:50618',
    'http://127.0.0.1:50619',
    'http://127.0.0.1:50620',
    'http://127.0.0.1:50748',  # Current browser preview port
    'http://127.0.0.1:50749',
    'http://127.0.0.1:50750',
    'http://localhost:50616',
    'http://localhost:50617',
    'http://localhost:50618',
    'http://localhost:50619',
    'http://localhost:50620',
    'http://localhost:50748',
    'http://localhost:50749',
    'http://localhost:50750',
    'https://planit.boramae.club',
    'http://planit.boramae.club',
]

# Additional CSRF settings for development
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_USE_SESSIONS = False

# For development only - disable CSRF for easier testing
# WARNING: Never use this in production!
CSRF_COOKIE_SECURE = False

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Development-specific logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
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
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'accounts': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
