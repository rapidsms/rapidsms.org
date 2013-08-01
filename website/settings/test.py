import sys
from .base import *

FLAG_EMAIL_ALERTS = ['info@example.com', ]
PROJECT_EMAIL_ALERTS = ['info@example.com', ]

DATABASES['default']['NAME'] = 'test_' + DATABASES['default']['NAME']

SECRET_KEY = 'asdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf'

GITHUB_KEY = 'key'
GITHUB_SECRET = 'secret'

