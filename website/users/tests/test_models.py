from django.test import TestCase

from ..models import User
from .factories import UserFactory


class UserTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory.create()

    def test_get_full_name(self):
        "Return either User.name or User.email"
        self.assertEqual(self.user.name, self.user.get_full_name())
        self.user.name = ''
        self.user.save()
        self.assertEqual(self.user.email, self.user.get_full_name())

    def test_user_type(self):
        "Check boolean for is_individual and is_organization return values"
        self.assertTrue(self.user.is_individual())
        self.assertFalse(self.user.is_organization())
        self.user.user_type = User.ORGANIZATION
        self.user.save()
        self.assertFalse(self.user.is_individual())
        self.assertTrue(self.user.is_organization())

    def test_create_user(self):
        "Test the custom UserManager for generating a non-superuser"
        email = 'foo@bar.com'
        name = 'John Doe'
        user = User.objects.create_user(email, 'asdfasdf', name)
        self.assertEqual(user.name, name)
        self.assertEqual(user.email, email)

    def test_create_user_invalid(self):
        "Test the custom UserManager for generating a non-superuser with errors"
        email = 'foo@bar.com'
        name = 'John Doe'
        with self.assertRaises(ValueError):
            User.objects.create_user(email=email, password='', name='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email=email, password='', name=name)
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='123', name=name)

    def test_create_superuser(self):
        "Test the custom UserManager for generating a superuser"
        email = 'foo@bar.com'
        name = 'John Doe'
        user = User.objects.create_superuser(email, 'asdfasdf', name)
        self.assertEqual(user.name, name)
        self.assertEqual(user.email, email)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_organization_unicode(self):
        "Return appropriate string for a User that identifies as an Organization"
        self.user.user_type = User.ORGANIZATION
        self.user.save()
        self.assertIn(User.USER_TYPES[User.ORGANIZATION], str(self.user))

    def test_user_unicode(self):
        """Test unicode representation for a user as an individual."""
        self.user.user_type = User.INDIVIDUAL
        self.user.save()
        self.assertEqual(self.user.get_full_name(), self.user.__unicode__())

    def test_get_absolute_url(self):
        """Test get_absolute_url for user"""
        expected = '/users/d/{pk}/'.format(pk=self.user.id)
        self.assertEqual(expected, self.user.get_absolute_url())

    def test_get_edit_url(self):
        """Test get_edit_url for user"""
        expected = '/users/d/{pk}/edit/'.format(pk=self.user.id)
        self.assertEqual(expected, self.user.get_edit_url())

    def test_get_short_name(self):
        "Test that get_short_name and get_full_name methods return the same"
        self.assertEqual(self.user.get_short_name(), self.user.get_full_name())

    def test_get_model_name(self):
        self.assertEqual(self.user.get_model_name(), 'user')
