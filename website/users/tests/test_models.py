import factory

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
