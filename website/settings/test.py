import sys
from .base import *

FLAG_EMAIL_ALERTS = []
PROJECT_EMAIL_ALERTS = []
DATABASES['default']['NAME'] = 'test_' + DATABASES['default']['NAME']

SECRET_KEY = 'asdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf'

GITHUB_KEY = 'key'
GITHUB_SECRET = 'secret'

