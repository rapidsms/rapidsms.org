import logging

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect
from django.views.generic import DetailView, UpdateView, FormView, ListView

from allaccess.models import AccountAccess
from allaccess.views import OAuthRedirect, OAuthCallback

from ..mixins import IsActiveMixin
from .forms import UserEditForm, UserRegistrationForm
from .models import User


logger = logging.getLogger(__name__)


class RapidSMSOAuthRedirect(OAuthRedirect):

    def get_callback_url(self, provider):
        return reverse('github_callback')

    def get_additional_parameters(self, provider):
        """Request read access to the user's email addresses."""
        return {
            'scope': 'user:email',
        }


class RapidSMSOAuthCallback(OAuthCallback):

    def get_primary_email(self, provider, access):
        """Retrieve the primary, verified email from the user's GitHub account."""
        # API endpoint for retrieving account emails from GitHub.
        email_url = 'https://api.github.com/user/emails'
        # Request v3 format that shows whether the email is verified.
        headers = {'Accept': 'application/vnd.github.v3'}
        response = access.api_client.request('GET', email_url, headers=headers)
        if response.status_code != 200:
            raise Exception('Error retrieving account emails.')
        emails = response.json()
        for email in emails:
            if email['verified'] and email['primary']:
                return email['email']
        return None

    def get_or_create_user(self, provider, access, info):
        """Try to find the user by their primary email address."""
        try:
            email = self.get_primary_email(provider, access)
        except:
            logger.exception()
            return None
        if not email:
            logger.error('User has no verified, primary email.')
            return None

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            try:
                kwargs = {
                    'email': email,
                    'name': info.get('name', info.get('login')),
                    'location': info.get('location', None),
                    'website_url': info.get('blog', None),
                    'github_url': info.get('html_url', None),
                }
                user = User(**kwargs)
                user.set_unusable_password()
                user.save()
            except Exception as e1:
                logger.exception()

                # Try excluding the extra information, in case that is
                # causing a validation or database error.
                logger.debug('Attempting to mitigate error by saving '
                        'the user without any additional information.')
                try:
                    user = User(email=email)
                    user.set_unusable_password()
                    user.save()
                except Exception as e2:
                    logger.exception()
                    logger.debug('Log in has failed.')
                    return None
                else:
                    logger.debug('Error was mitigated; log in continues.')
        return user

    def handle_new_user(self, provider, access, info):
        user = self.get_or_create_user(provider, access, info)
        if not user:
            return self.handle_login_failure(provider, 'Could not create user.')
        access.user = user
        AccountAccess.objects.filter(pk=access.pk).update(user=user)
        user = authenticate(provider=access.provider, identifier=access.identifier)
        login(self.request, user)
        return redirect(self.get_login_redirect(provider, user, access, True))


class Registration(FormView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        password = form.cleaned_data['password1']
        user = authenticate(username=user.email, password=password)
        login(self.request, user)
        messages.success(request, 'Thanks for registering for RapidSMS.org!')
        return redirect(self.get_success_url())


class UserDetail(IsActiveMixin, DetailView):
    model = User


class UserEdit(IsActiveMixin, UpdateView):
    model = User
    form_class = UserEditForm

    def get_object(self, queryset=None):
        obj = super(UserEdit, self).get_object(queryset)
        if obj != self.request.user:
            raise Http404()
        return obj
