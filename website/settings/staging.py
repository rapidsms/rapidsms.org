from website.settings.base import *

import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ['SECRET_KEY']

DATABASES['default']['NAME'] = 'website_staging'

PUBLIC_ROOT = '/var/www/website-staging/public/'

STATIC_ROOT = os.path.join(PUBLIC_ROOT, 'static')

MEDIA_ROOT = os.path.join(PUBLIC_ROOT, 'media')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

EMAIL_SUBJECT_PREFIX = '[Website Staging] '

COMPRESS_ENABLED = True

SESSION_COOKIE_SECURE = True

SESSION_COOKIE_HTTPONLY = True

ALLOWED_HOSTS = ('*',)

GITHUB_KEY = os.environ['GITHUB_KEY']
GITHUB_SECRET = os.environ['GITHUB_SECRET']
SUPERFEEDR_CREDS = os.environ['SECRET_KEY']
BROKER_URL = 'amqp://website:%s@127.0.0.1:5672/website_staging' % os.environ['BROKER_PASSWORD']

FLAG_EMAIL_ALERTS = ['rapidsms-team@caktusgroup.com']
