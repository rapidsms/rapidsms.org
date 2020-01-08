from website.datamaps.models import Country
from django.test import TestCase

from ..factories import UserFactory
from ..forms import UserCreationForm
from ..forms import UserChangeForm
from ..forms import UserEditForm
from ..forms import UserRegistrationForm
from ..models import User

__all__ = ["UserCreationFormTest", "UserChangeFormTest", "UserEditFormTest",
    "UserRegistrationFormTest", ]


class UserCreationFormTest(TestCase):

    def setUp(self):
        self.form = UserCreationForm
        self.user = UserFactory.create()

    def _get_invalid_data(self):
        data = {
            "email": self.user.email,
            "password1": "password",
            "password2": "password",
        }
        return data

    def _get_valid_data(self):
        data = {
            "email": "somenewemail@example.com",
            "password1": "password",
            "password2": "password",
        }
        return data

    def test_init_pop_user_name(self):
        form = self.form()
        self.assertNotIn("username", form.fields)

    def test_init_pop_user_error(self):
        form = self.form(data=self._get_invalid_data)
        self.assertNotIn("duplicate_username", form.error_messages)

    def test_init_duplicate_email_message(self):
        form = self.form()
        self.assertEqual(
            "A user with that email address already exists.",
            form.error_messages['duplicate_email']
        )

    def test_meta(self):
        self.assertEqual(self.form._meta.model, User)
        self.assertEqual(self.form._meta.fields, ('email', ))

    def test_clean_email_user_does_not_exists(self):
        data = self._get_valid_data()
        form = self.form(data=data)
        self.failIf(form.errors)
        self.assertEqual(form.clean_email(), data['email'])

    def test_clean_email_user_exists(self):
        data = self._get_invalid_data()
        form = self.form(data=data)
        self.failUnless(form.errors)
        self.assertIn("email", form.errors)

    def test_valid(self):
        form = self.form(data=self._get_valid_data())
        self.failUnless(form.is_valid())


class UserChangeFormTest(TestCase):

    def setUp(self):
        self.form = UserChangeForm

    def test_init(self):
        form = self.form()
        self.assertNotIn("username", form.fields)

    def test_meta(self):
        self.assertEqual(self.form._meta.model, User)


class UserEditFormTest(TestCase):

    fixtures = ['countries.json']  # Loads initial django-datamaps data

    def setUp(self):
        self.form = UserEditForm
        self.user = UserFactory.create()

    def _get_valid_data(self):
        data = {
            "user_type": "I",
            "name": "User",
            "email": self.user.email,
            "for_hire": True,
            "password1": "password",
            "password2": "password",
        }
        return data

    def _get_invalid_data(self):
        data = {
            "user_type": "I",
            "name": "User",
            "email": self.user.email,
            "for_hire": True,
            "password1": "password",
            "password2": "password2",
        }
        return data

    def test_country_validate_select(self):
        "Test that a valid selection from the django-select widget validates"
        us = Country.objects.get(name="United States of America")
        data = self._get_valid_data()
        data.update(
            {"country_1": us.pk, "country_0": "United States of America", }
        )
        form = self.form(data=data, instance=self.user)
#        import pdb; pdb.set_trace();
        self.failUnless(form.is_valid())
        self.assertEqual(form.cleaned_data['country'], us)

    def test_country_validate_manual(self):
        "Test that a valid manually entered country name validates"
        us = Country.objects.get(name="United States of America")
        data = self._get_valid_data()
        data.update(
            {"country_0": "united states of america", }
        )
        form = self.form(data=data, instance=self.user)
#        import pdb; pdb.set_trace();
        self.failUnless(form.is_valid())
        self.assertEqual(form.cleaned_data['country'], us)

    def test_country_invalidate_manual(self):
        "Test that a invalid manually entered country name does not validate"
        data = self._get_valid_data()
        data.update(
            {"country_0": "united states aaaaa", }
        )
        form = self.form(data=data, instance=self.user)
        self.failIf(form.is_valid())
        self.assertIn('country', form.errors)

    def test_meta_model(self):
        self.assertEqual(self.form._meta.model, User)

    def test_meta_fields(self):
        expected = ('user_type', 'name', 'location', 'country', 'email',
                'display_email', 'biography', 'website_url', 'github_url',
                'gravatar_email', 'avatar', 'for_hire', 'password1',
                'password2')
        self.assertEqual(expected, self.form._meta.fields)

    def test_init(self):
        form = self.form(instance=self.user)
        self.assertNotIn('password', form.fields)

    def test_clean_password2(self):
        data = self._get_valid_data()
        form = self.form(data=data, instance=self.user)
        self.failIf(form.errors)
        self.assertEqual(form.clean_password2(), data["password2"])

    def test_password_mismatch(self):
        data = self._get_invalid_data()
        form = self.form(data=data, instance=self.user)
        self.failIf(form.is_valid())
        self.assertIn('password2', form.errors)


class UserRegistrationFormTest(TestCase):

    fixtures = ['countries.json']  # Loads initial django-datamaps data

    def setUp(self):
        self.form = UserRegistrationForm

    def _get_valid_data(self):
        data = {
            "user_type": "I",
            "name": "User",
            "email": "newuser@example.com",
            "for_hire": True,
            "password1": "password",
            "password2": "password",
        }
        return data

    def test_init(self):
        form = self.form()
        self.assertIn('duplicate_email', form.error_messages)
        self.assertEqual('Password', form.fields['password1'].label)
        self.assertEqual('Confirm Password', form.fields['password2'].label)

    def test_meta_model(self):
        self.assertEqual(self.form._meta.model, User)

    def test_meta_fields(self):
        expected = ('user_type', 'name', 'location', 'country', 'email',
                'display_email', 'biography', 'website_url', 'github_url',
                'gravatar_email', 'avatar', 'for_hire')
        self.assertEqual(expected, self.form._meta.fields)

    def test_country_validate_select(self):
        "Test that a valid selection from the django-select widget validates"
        us = Country.objects.get(name="United States of America")
        data = self._get_valid_data()
        data.update(
            {"country_1": us.pk, "country_0": "United States of America", }
        )
        form = self.form(data=data)
#        import pdb; pdb.set_trace();
        self.failUnless(form.is_valid())
        self.assertEqual(form.cleaned_data['country'], us)

    def test_country_validate_manual(self):
        "Test that a valid manually entered country name validates"
        us = Country.objects.get(name="United States of America")
        data = self._get_valid_data()
        data.update(
            {"country_0": "united states of america", }
        )
        form = self.form(data=data)
#        import pdb; pdb.set_trace();
        self.failUnless(form.is_valid())
        self.assertEqual(form.cleaned_data['country'], us)

    def test_country_invalidate_manual(self):
        "Test that a invalid manually entered country name does not validate"
        data = self._get_valid_data()
        data.update(
            {"country_0": "united states aaaaa", }
        )
        form = self.form(data=data)
        self.failIf(form.is_valid())
        self.assertIn('country', form.errors)
