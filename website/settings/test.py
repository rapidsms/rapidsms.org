from .base import *

DATABASES['default']['NAME'] = 'test_' + DATABASES['default']['NAME']

SECRET_KEY = 'asdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf'

GITHUB_KEY = 'key'
GITHUB_SECRET = 'secret'
