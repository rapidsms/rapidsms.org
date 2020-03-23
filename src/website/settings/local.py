import uuid

from website.settings.base import *

uuid._uuid_generate_random = None

COMPRESS_ENABLED = False
