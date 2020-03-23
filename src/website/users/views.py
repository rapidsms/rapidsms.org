import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView

from ..mixins import IsActiveObjectMixin, LoginRequiredMixin
from .forms import UserEditForm, UserRegistrationForm
from .models import User

# from allaccess.models import AccountAccess
# from allaccess.views import OAuthRedirect, OAuthCallback


logger = logging.getLogger(__name__)


# class RapidSMSOAuthRedirect(OAuthRedirect):
#
#     def get_callback_url(self, provider):
#         return reverse('github_callback')
#
#     def get_additional_parameters(self, provider):
#         """Request read access to the user's email addresses."""
#         return {
#             'scope': 'user:email',
#         }


# class RapidSMSOAuthCallback(OAuthCallback):
#
#     def get_primary_email(self, provider, access):
#         """Retrieve the primary, verified email from the user's GitHub account."""
#         # API endpoint for retrieving account emails from GitHub.
#         email_url = 'https://api.github.com/user/emails'
#         # Request v3 format that shows whether the email is verified.
#         headers = {'Accept': 'application/vnd.github.v3'}
#         # import pdb; pdb.set_trace()
#         response = access.api_client.request('GET', email_url, headers=headers)
#         if response.status_code != 200:
#             raise Exception('Error retrieving account emails.')
#         emails = response.json()
#         for email in emails:
#             if email['verified'] and email['primary']:
#                 return email['email']
#         messages.error(self.request,
#                        'Your email address could not be verified!')
#         return None
#
#     def get_or_create_user(self, provider, access, info):
#         """Try to find the user by their primary email address."""
#         try:
#             # import pdb; pdb.set_trace()
#             email = self.get_primary_email(provider, access)
#         except:
#             logger.exception("Client time out.")
#             return None
#         if not email:
#             logger.error('User has no verified, primary email.')
#             return None
#
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             try:
#                 kwargs = {
#                     'email': email,
#                     'name': info.get('name', info.get('login')),
#                     'location': info.get('location', None),
#                     'website_url': info.get('blog', None),
#                     'github_url': info.get('html_url', None),
#                 }
#                 user = User(**kwargs)
#                 user.set_unusable_password()
#                 user.save()
#             except Exception as e1:
#                 logger.exception(e1)
#
#                 # Try excluding the extra information, in case that is
#                 # causing a validation or database error.
#                 logger.debug('Attempting to mitigate error by saving '
#                         'the user without any additional information.')
#                 try:
#                     user = User(email=email)
#                     user.set_unusable_password()
#                     user.save()
#                 except Exception as e2:
#                     logger.exception(e2)
#                     logger.debug('Log in has failed.')
#                     return None
#                 else:
#                     logger.debug('Error was mitigated; log in continues.')
#         return user
#
#     def handle_new_user(self, provider, access, info):
#         user = self.get_or_create_user(provider, access, info)
#         if not user:
#             return self.handle_login_failure(provider, 'Could not create user.')
#         access.user = user
#         AccountAccess.objects.filter(pk=access.pk).update(user=user)
#         user = authenticate(provider=access.provider, identifier=access.identifier)
#         login(self.request, user)
#         return redirect(self.get_login_redirect(provider, user, access, True))


class Registration(FormView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        password = form.cleaned_data['password1']
        user = authenticate(username=user.email, password=password)
        login(self.request, user)
        messages.success(self.request, 'Thanks for registering for RapidSMS.org!')
        return redirect(self.get_success_url())


class UserDetail(IsActiveObjectMixin, DetailView):
    model = User


class UserEdit(LoginRequiredMixin, IsActiveObjectMixin, UpdateView):
    model = User
    form_class = UserEditForm

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj != self.request.user:
            raise PermissionDenied
        return obj
