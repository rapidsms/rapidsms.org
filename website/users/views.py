import base64
import hashlib

from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, UpdateView

from allaccess.compat import smart_bytes, force_text
from allaccess.views import OAuthRedirect, OAuthCallback

from .models import User


class RapidSMSOAuthRedirect(OAuthRedirect):

    def get_callback_url(self, provider):
        return reverse('github-callback')

    def get_additional_parameters(self, provider):
        return {
            'scope': 'user:email',
        }


class RapidSMSOAuthCallback(OAuthCallback):
    # API endpoint for retrieving account emails from Github.
    email_url = 'https://api.github.com/user/emails'

    def get_user_emails(self, provider, access):
        """
        Retrieve a list of emails associated with the user's Github account.
        """
        response = access.api_client.request('GET', self.email_url)
        if response.status_code != 200:
            raise Exception('Error retrieving account emails.')
        return response.json()

    def get_or_create_user(self, provider, access, info):
        emails = self.get_user_emails(provider, access)
        if not emails:
            raise Exception('No emails associated with account?')
        if len(emails) > 1:
            pass  # TODO - send user to disambiguation page?
        email = emails[0]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            digest = hashlib.sha1(smart_bytes(access)).digest()
            username = force_text(base64.urlsafe_b64encode(digest)).replace('=','')
            kwargs = {
                'user_type': User.INDIVIDUAL,
                'username': username,
                'email': email,
                'location': info['location'],
                'website_url': info['blog'],
                'github_url': info['html_url'],
            }
            user = User(**kwargs)
            user.set_unusable_password()
            user.save()
        return user

    def get_login_redirect(self, provider, user, access, new=False):
        return reverse('home')


class UserDetail(DetailView):
    model = User
    context_object_name = 'user'


class UserEdit(UpdateView):
    model = User
    context_object_name = 'user'


class UserList(ListView):
    model = User
