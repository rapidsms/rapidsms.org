from django import forms
from django.contrib.auth import forms as auth
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from .models import User


class UserCreationForm(auth.UserCreationForm):
    """Modified form that uses our custom User model."""

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields.pop('username')
        if 'duplicate_username' in self.error_messages:
            self.error_messages.pop('duplicate_username')
        self.error_messages['duplicate_email'] = 'A user with that email '\
                'address already exists.'

    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            self._meta.model._default_manager.get(email=email)
        except self._meta.model.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])


class UserChangeForm(auth.UserChangeForm):
    """Modified form that uses our custom User model."""

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields.pop('username')

    class Meta:
        model = User


class UserRegistrationForm(UserCreationForm):
    user_type = forms.ChoiceField(label='Register as an...',
            widget=forms.RadioSelect, choices=User.USER_TYPES.items())

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.error_messages['duplicate_email'] = mark_safe('There is already '
                'an account associated with this email address.<br /> If this '
                'is your email, you can try to <a href="{login}">log in with '
                'your email address or GitHub account</a> or '
                '<a href="{reset}">reset your password</a>.'.format(**{
                    'login': reverse('login'),
                    'reset': reverse('reset_password'),
                    'github': reverse('github_login'),
                }))
        self.fields['country'].empty_label = 'Country'
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'
        self.fields['for_hire'].label = 'Are you available for '\
                'RapidSMS-related hire or consulting?'

    class Meta:
        model = User
        fields = ('user_type', 'name', 'location', 'country', 'email',
                'website_url', 'github_url', 'for_hire')
