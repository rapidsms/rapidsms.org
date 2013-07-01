from website.settings.staging import *

# There should be only minor differences from staging

DATABASES['default']['NAME'] = 'website_production'

PUBLIC_ROOT = '/var/www/website-production/public/'

STATIC_ROOT = os.path.join(PUBLIC_ROOT, 'static')

MEDIA_ROOT = os.path.join(PUBLIC_ROOT, 'media')

EMAIL_SUBJECT_PREFIX = '[Website Prod] '

BROKER_URL = 'amqp://website:%s@127.0.0.1:5672/website_production' % os.environ['BROKER_PASSWORD']
