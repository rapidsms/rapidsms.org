"""Django settings for website project."""
import os
from pathlib import Path

import environ
from django.urls import reverse_lazy

env = environ.Env()
environ.Env.read_env()

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PROJECT_ROOT = os.path.abspath(os.path.join(PROJECT_PATH, os.pardir))

DEBUG = env.bool('DEBUG', False)

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {'default': env.db()}
SECRET_KEY = env.str('SECRET_KEY', '')

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'public', 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'public', 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
SETTINGS_DIR = Path(__file__).parent
PACKAGE_DIR = SETTINGS_DIR.parent
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(PACKAGE_DIR / 'templates')
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'staticfiles': 'django.templatetags.static',
                'i18n': 'django.templatetags.i18n',
            },
        },
    },
]

# # List of callables that know how to import templates from various sources.
# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
# #     'django.template.loaders.eggs.Loader',
# )
#
# TEMPLATE_CONTEXT_PROCESSORS = (
#     'django.contrib.auth.context_processors.auth',
#     'django.contrib.messages.context_processors.messages',
#     'django.core.context_processors.debug',
#     'django.core.context_processors.media',
#     'django.core.context_processors.request',
#     'django.core.context_processors.i18n',
#     'django.core.context_processors.static',
# )
#
# TEMPLATE_DIRS = (
#     os.path.join(PROJECT_PATH, 'templates'),
# )


MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'website.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'website.wsgi.application'


FIXTURE_DIRS = (
    os.path.join(PROJECT_PATH, 'fixtures'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.sitemaps',

    # External apps that other apps depend on
    'website.datamaps',
    'website.taxonomy',
    'website.aggregator',
    'website.projects',
    'website.packages',
    'website.users',
    'website.website_tests',

    # External apps
    # 'south',
    'compressor',
    'scribbler',
    'widget_tweaks',
    'sorl.thumbnail',
    'selectable',
    'celery',
    'taggit',
    'django_push.subscriber',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Application settings

# COMPRESS_URL =
COMPRESS_URL = r'%s/public/static/' % os.path.abspath(os.path.dirname(__file__))
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # 'allaccess.backends.AuthorizedServiceBackend',
]

AUTH_USER_MODEL = 'users.User'
LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('home')

CELERY_TASK_ALWAYS_EAGER = False

DEFAULT_FROM_EMAIL = 'no-reply@rapidsms.org'

# PubSubHubbub settings
FEED_APPROVERS_GROUP_NAME = "feed-approver"
SUPERFEEDR_CREDS = []  # set in production/staging/local.py
PUSH_HUB = 'https://superfeedr.com/hubbub'
PUSH_CREDENTIALS = 'website.aggregator.utils.push_credentials'

# Maximum number of projects to show on the map
# MAX_NUM_PROJECTS = 5

ALLOWED_TAGS = ('a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i',
                'li', 'ol', 'strong', 'ul', 'font', 'div', 'span', 'br',
                'strike', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'table',
                'tr', 'td', 'th', 'thead', 'tbody', 'dl', 'dd', )

ALLOWED_ATTRIBUTES = {'*': ['class'], 'a': ['href', 'title'],
                      'abbr': ['title'], 'acronym': ['title'],
                      'font': ['face', 'size',], 'div': ['style', ],
                      'span': ['style', ], 'ul': ['style', ], }

ALLOWED_STYLES = ['font-size', 'color', 'text-align', 'text-decoration',
                  'font-weight', ]
