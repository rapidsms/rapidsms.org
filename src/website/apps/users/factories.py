import os

from django.core.files import File

import factory

from .models import User

__all__ = ['TEST_IMAGE', 'UserFactory', 'UserWithAvatarFactory']


TEST_IMAGE = os.path.join(os.path.dirname(__file__), 'test.png')


class UserFactory(factory.DjangoModelFactory):

    name = factory.Sequence(lambda n: 'user%s' % n)
    email = factory.LazyAttribute(lambda obj: '%s@example.com' % obj.name)

    class Meta:
        model = User


class UserWithAvatarFactory(UserFactory):
    avatar = factory.LazyAttribute(lambda t: File(open(TEST_IMAGE)))
