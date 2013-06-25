import factory
import os

from django.core.files import File

from ..models import User


TEST_IMAGE = os.path.join(os.path.dirname(__file__), 'test.png')


class UserFactory(factory.Factory):
    FACTORY_FOR = User

    name = factory.Sequence(lambda n: 'user%s' % n)
    email = factory.LazyAttribute(lambda obj: '%s@example.com' % obj.name)


class UserAvatarFactory(UserFactory):
    avatar = factory.LazyAttribute(lambda t: File(open(TEST_IMAGE)))
