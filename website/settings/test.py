from .base import *

DATABASES['default']['NAME'] = 'test_' + DATABASES['default']['NAME']

SECRET_KEY = 'asdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf'

GITHUB_KEY = 'key'
GITHUB_SECRET = 'secret'

CELERY_ALWAYS_EAGER = True

COMPRESS_ENABLED = False

COMPRESS_PRECOMPILERS = ()

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
