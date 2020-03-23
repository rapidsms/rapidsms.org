import uuid
uuid._uuid_generate_random = None

from website.settings.base import *


DATABASES['default']['NAME'] = 'rapidpro_community_portal_1'
DATABASES['default']['USER'] = 'postgres'
DATABASES['default']['PASSWORD'] = ''

COMPRESS_ENABLED = False
