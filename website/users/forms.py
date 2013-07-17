from django import forms
from django.contrib.auth import forms as auth
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from selectable.forms import AutoCompleteSelectField

from ..projects.lookups import CountryLookup
from ..projects.models import Country
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


class UserEditForm(UserChangeForm):
    password1 = forms.CharField(label='New Password', required=False,
            widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirm', required=False,
            widget=forms.PasswordInput, help_text='Enter the same password '
            'as above, for verification.')
    country = AutoCompleteSelectField(lookup_class=CountryLookup, required=False)

    class Meta:
        model = User
        fields = ('user_type', 'name', 'location', 'country', 'email',
                'display_email', 'biography', 'website_url', 'github_url',
                'gravatar_email', 'avatar', 'for_hire', 'password1',
                'password2')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields.pop('password', None)

    def clean_country(self):
        """ Validate country selected

            django-selectable allows for non-validated data to be submitted
            without raising a ValidationError. This method verifies that a
            country exists when inputed manually.

        """
        country = self.cleaned_data["country"]
        user_input = self.data.get('country_0', None)
        if user_input and not country:
            # If a user inputs the name of country manually (instead of
            # selecting it from django-select's drop-down menu, existance of
            # the country needs to be verified.
            try:
                country = Country.objects.get(name__iexact=user_input)
            except Country.DoesNotExist:
                raise forms.ValidationError("Please select a valid country.")
        return country

    # TODO: change validation error to string or add a error_messages dict at
    # __init__
    def clean_password2(self):
        """Require that passwords match."""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(u"Verify that both passwords match.")
        return password2


class UserRegistrationForm(UserCreationForm):
    user_type = forms.ChoiceField(label='Account Type',
            widget=forms.RadioSelect, choices=User.USER_TYPES.items())
    country = AutoCompleteSelectField(lookup_class=CountryLookup, required=False)

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
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'

    class Meta:
        model = User
        fields = ('user_type', 'name', 'location', 'country', 'email',
                'display_email', 'biography', 'website_url', 'github_url',
                'gravatar_email', 'avatar', 'for_hire',)

    def clean_country(self):
        """ Validate country selected


            django-selectable allows for non-validated data to be submitted
            without raising a ValidationError. This method verifies that a
            country exists when inputed manually.

        """
        country = self.cleaned_data.get("country")
        user_input = self.data.get('country_0')
        if user_input and not country:
            # If a user inputs the name of country manually (instead of
            # selecting it from the django-select's drop-down menu, existance of
            # the country needs to be verified.
            try:
                country = Country.objects.get(name__iexact=user_input)
            except Country.DoesNotExist:
                raise forms.ValidationError("Please select a valid country.")
        return country
