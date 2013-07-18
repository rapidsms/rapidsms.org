from django.test import TestCase
from django.core.urlresolvers import reverse_lazy

from ..views import RapidSMSOAuthRedirect

__all__ = ['RapidSMSOAuthRedirectTest', ]


class RapidSMSOAuthRedirectTest(TestCase):
    """Test for RapidSMSOAuthRedirect view"""

    url = reverse_lazy('github_login')
    callback_url = reverse_lazy('github_callback')

    def setUp(self):
        self.view = RapidSMSOAuthRedirect()

    def test_get_call_back_url(self):
        self.assertEqual(
            self.view.get_callback_url("github"),
            self.callback_url
        )

    def test_get_additional_parameters(self):
        parameters = self.view.get_additional_parameters("github")
        self.assertEqual('user:email', parameters['scope'])

    def test_GET(self):
        response = self.client.get(self.url)
