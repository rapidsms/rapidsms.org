from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class RapidSMSAdminUserCreationForm(UserCreationForm):
    """Modified Admin form that uses our custom User model."""

    class Meta:
        model = User

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            self._meta.model._default_manager.get(username=username)
        except self._meta.model.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


class RapidSMSAdminUserChangeForm(UserChangeForm):
    """Modified Admin form that uses our custom User model."""

    class Meta:
        model = User
