import sys

from website.settings.base import *


FLAG_EMAIL_ALERTS = ['info@example.com', ]
PROJECT_EMAIL_ALERTS = ['info@example.com', ]

INTERNAL_IPS = ('127.0.0.1', )


INSTALLED_APPS += ('debug_toolbar',)
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False
}


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SOUTH_TESTS_MIGRATE = True

COMPRESS_ENABLED = False

# import celery
# djcelery.setup_loader()

CELERY_ALWAYS_EAGER = True

# Special test settings
if 'test' in sys.argv:
    CELERY_ALWAYS_EAGER = True

    COMPRESS_ENABLED = False

    COMPRESS_PRECOMPILERS = ()

    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.SHA1PasswordHasher',
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )
