from django.conf import settings
from django.core.urlresolvers import reverse_lazy, reverse
from mock import patch
from mock import PropertyMock

from website.tests.base import ViewTestMixin, WebsiteTestBase
from ..models import User
from ..views import RapidSMSOAuthRedirect, RapidSMSOAuthCallback
from .base import MockClient

__all__ = ['RapidSMSOAuthRedirectTest', 'RapidSMSOAuthCallbackTest',
           'RegistrationTest', ]


class RapidSMSOAuthRedirectTest(ViewTestMixin, WebsiteTestBase):
    """Test for RapidSMSOAuthRedirect view. Users should be redirected to
    providers login page."""
    fixtures = ['test_provider.json', ]  # Creates a sample github's provider
    url = reverse_lazy('github_login')

    def test_get_unauthenticated(self):
        client = MockClient(name='github')
        with patch.object(RapidSMSOAuthRedirect, 'get_client') as github_client:
            github_client.return_value = client
            response = self._get(url=self.url)
            self.assertRedirectsNoFollow(response, client.url)


class RapidSMSOAuthCallbackTest(ViewTestMixin, WebsiteTestBase):
    """Tests what happens after a user has come back from a provider.
    New user should be created and associate with user account if it doesn't
    already exists. Users should be authenticated.
    """
    fixtures = ['test_provider.json', ]  # Creates a sample github's provider
    url = reverse_lazy('github_callback')

    def test_new_user_verified_email(self):
        """A new user should be created and authenticated."""
        client = MockClient(name='github', response=[{'verified': True,
                'primary': True, 'email': 'info@example.com'}])
        with patch.object(RapidSMSOAuthCallback, 'get_client') as github_client:
            github_client.return_value = client
            with patch('allaccess.models.AccountAccess.api_client',
                       new_callable=PropertyMock) as access_api:
                    access_api.return_value = client
                    # access_api.assert_called_once_with()
                    response = self._get(url=self.url)
                    # New user should have been created
                    user = User.objects.get(email='info@example.com')
                    self.failUnless(user.id)
                    self.assertRedirectsNoFollow(response,
                        settings.LOGIN_REDIRECT_URL.decode())

    def test_new_user_unverified_email(self):
        """If a github users has a unverified email address no user should be
        created.
        """
        client = MockClient(name='github', response=[{'verified': False,
                'primary': False, 'email': 'info@example.com'}])
        with patch.object(RapidSMSOAuthCallback, 'get_client') as github_client:
            github_client.return_value = client
            with patch('allaccess.models.AccountAccess.api_client',
                       new_callable=PropertyMock) as access_api:
                    access_api.return_value = client
                    # access_api.assert_called_once_with()
                    response = self._get(url=self.url)
                    # New user should have been created
                    self.assertRaises(User.DoesNotExist, User.objects.get,
                                      email='info@example.com')
                    self.assertRedirectsNoFollow(response,
                        settings.LOGIN_URL.decode())

    def test_get_primary_email_raises_exception(self):
        client = MockClient(name='github', response_status=500)
        with patch.object(RapidSMSOAuthCallback, 'get_client') as github_client:
            github_client.return_value = client
            with patch('allaccess.models.AccountAccess.api_client',
                       new_callable=PropertyMock) as access_api:
                    access_api.return_value = client
                    # access_api.assert_called_once_with()
                    response = self._get(url=self.url)
                    # New user should have been created
                    self.assertRaises(User.DoesNotExist, User.objects.get,
                                      email='info@example.com')
                    self.assertRedirectsNoFollow(response,
                        settings.LOGIN_URL.decode())


class RegistrationTest(ViewTestMixin, WebsiteTestBase):
    """Tests that a user can register to the website."""
    url_name = 'register'
    template_name = 'users/registration.html'

    def get_form_data(self):
        data = {
            'user_type': User.INDIVIDUAL,
            'name': 'User 1',
            'email': 'info@example.com',
            'display_email': True,
            'password1': 'password',
            'password2': 'password'
        }
        return data

    def test_get_unauthenticated(self):
        response = self._get()
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.failUnless('form' in response.context)

    def test_post_unauthenticated(self):
        data = self.get_form_data()
        response = self._post(data=data)  # User is creatd
        user = User.objects.get(email=data['email'])
        self.failUnless(user.id)
        self.assertRedirectsNoFollow(response,
                                     settings.LOGIN_REDIRECT_URL.decode())
