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
        """Request read access to the user's email addresses."""
        return {
            'scope': 'user:email',
        }


class RapidSMSOAuthCallback(OAuthCallback):

    def get_verified_user_emails(self, provider, access):
        """Retrieve a list of emails that the user has verified with Github."""
        # API endpoint for retrieving account emails from Github.
        email_url = 'https://api.github.com/user/emails'
        # Request v3 format that shows whether the email is verified.
        headers = {'Accept': 'application/vnd.github.v3'}
        response = access.api_client.request('GET', email_url, headers=headers)
        if response.status_code != 200:
            raise Exception('Error retrieving account emails.')
        emails = response.json()
        return [email['email'] for email in emails if email['verified']]

    def get_or_create_user(self, provider, access, info):
        emails = self.get_verified_user_emails(provider, access)
        if not emails:
            # FIXME - Show error page.
            raise Exception('Account has no verified emails?')
        if len(emails) > 1:
            # FIXME - Show a disambiguation page.
            pass
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
