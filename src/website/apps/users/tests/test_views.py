from django.urls import reverse

from website.apps.tests.base import ViewTestMixin, WebsiteTestBase

from ..models import User


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
        self.assertRedirectsNoFollow(response, reverse('home'))
