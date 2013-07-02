from .base import *

DATABASES['default']['name'] = 'test_' + DATABASES['default']['name']

SECRET_KEY = 'asdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf'

GITHUB_KEY = 'key'
GITHUB_SECRET = 'secret'
