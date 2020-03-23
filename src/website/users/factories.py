import factory
import os

from django.core.files import File

from .models import User


__all__ = ['TEST_IMAGE', 'UserFactory', 'UserWithAvatarFactory']


TEST_IMAGE = os.path.join(os.path.dirname(__file__), 'test.png')


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    name = factory.Sequence(lambda n: 'user%s' % n)
    email = factory.LazyAttribute(lambda obj: '%s@example.com' % obj.name)


class UserWithAvatarFactory(UserFactory):
    avatar = factory.LazyAttribute(lambda t: File(open(TEST_IMAGE)))