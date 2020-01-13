from .settings_common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Setup Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    # Logger
    'loggers': {
        # Django
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },

        # demand_manager
        'demand_manager': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },

    # Handler
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'dev',
        },
    },

    # Formatter
    'formatters': {
        'dev': {
            'format': '\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(Line:%(lineno)d)',
                '%(message)s'
            ])
        },
    },
}

# Email Setup for Develop
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'