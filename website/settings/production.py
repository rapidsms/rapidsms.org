from website.settings.staging import *

# There should be only minor differences from staging

DATABASES['default']['NAME'] = 'website_production'

EMAIL_SUBJECT_PREFIX = '[Website Prod] '

