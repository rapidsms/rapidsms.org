from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, UpdateView

from allaccess.views import OAuthRedirect, OAuthCallback

from .models import User


class RapidSMSOAuthRedirect(OAuthRedirect):

    def get_callback_url(self, provider):
        return reverse('github-callback')


class RapidSMSOAuthCallback(OAuthCallback):

    def get_or_create_user(self, provider, access, info):
        email = info['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            digest = hashlib.sha1(smart_bytes(access)).digest()
            username = force_text(base64.urlsafe_b64encode(digest)).replace('=','')
            kwargs = {
                'username': username,
                'email': email,
                'location': info['location'],
                'website_url': info['blog'],
                'github_url': info['html_url'],
                'password': None,
            }
            user = User.objects.create(**kwargs)
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
