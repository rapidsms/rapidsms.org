from django.contrib.auth.views import password_reset_confirm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, UpdateView, FormView

from allaccess.views import OAuthRedirect, OAuthCallback

from .forms import UserEditForm, UserRegistrationForm
from .models import User


class RapidSMSOAuthRedirect(OAuthRedirect):

    def get_callback_url(self, provider):
        return reverse('github_callback')

    def get_additional_parameters(self, provider):
        """Request read access to the user's email addresses."""
        return {
            'scope': 'user:email',
        }


class RapidSMSOAuthCallback(OAuthCallback):

    def get_verified_user_emails(self, provider, access):
        """Retrieve a list of emails that the user has verified with GitHub."""
        # API endpoint for retrieving account emails from GitHub.
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
        return user


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


class UserDetail(DetailView):
    model = User


class UserEdit(UpdateView):
    model = User
    form_class = UserEditForm

    def get_object(self, queryset=None):
        obj = super(UserEdit, self).get_object(queryset)
        if obj != self.request.user:
            raise Http404()
        return obj


class UserList(ListView):
    model = User
