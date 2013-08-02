import sys

from website.settings.base import *


FLAG_EMAIL_ALERTS = ['info@example.com', ]
PROJECT_EMAIL_ALERTS = ['info@example.com', ]

DEBUG = True
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = ('127.0.0.1', )


# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ['SECRET_KEY']


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

# Special test settings
if 'test' in sys.argv:
    CELERY_ALWAYS_EAGER = True

    COMPRESS_ENABLED = False

    COMPRESS_PRECOMPILERS = ()

    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.SHA1PasswordHasher',
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )
