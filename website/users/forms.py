from django import forms
from django.contrib.auth import forms as auth

from .models import User


class UserCreationForm(auth.UserCreationForm):
    """Modified form that uses our custom User model."""
    error_messages = {
        'duplicate_email': 'A user with that email already exists.',
        'password_mismatch': 'The two password fields didn\'t match.',
    }

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields.pop('username')

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
