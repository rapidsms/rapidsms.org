from website.settings.base import *

from datetime import timedelta

import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG


ADMINS = (
    ('Evan Wheeler', 'evanmwheeler@gmail.com'),
    ('Colin Copeland', 'copelco@caktusgroup.com'),
    ('RapidSMS.org Caktus Team', 'rapidsms-team@caktusgroup.com'),
)
MANAGERS = ADMINS

FLAG_EMAIL_ALERTS = ['evanmwheeler@gmail.com',
                     'copelco@caktusgroup.com',
                     'rapidsms-team@caktusgroup.com']
PROJECT_EMAIL_ALERTS = FLAG_EMAIL_ALERTS

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
SUPERFEEDR_CREDS = (os.environ['SUPERFEEDR_USER'], os.environ['SUPERFEEDR_PWD'])
PUSH_SSL_CALLBACK = True

#celery settings
import djcelery
djcelery.setup_loader()
BROKER_URL = 'amqp://website:%s@127.0.0.1:5672/website_staging' % os.environ['BROKER_PASSWORD']
CELERYBEAT_SCHEDULE = {
    'update-packages-every-hour': {
        'task': 'website.packages.update_packages',
        'schedule': timedelta(hours=1),
    },
}
