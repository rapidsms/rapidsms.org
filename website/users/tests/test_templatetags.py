from hashlib import md5

from django.test import TestCase

from ..templatetags.user_tags import gravatar_url


class TemplateTagsTestCase(TestCase):

    def test_gravatar_url(self):
        email = 'john@doe.com'
        bits = md5(email.lower()).hexdigest()
        url = gravatar_url(email)
        self.assertIn(bits, url)
