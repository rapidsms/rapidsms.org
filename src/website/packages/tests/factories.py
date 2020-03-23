import factory

from website.users.factories import UserFactory

from ..models import Package


__all__ = ['PackageFactory']


class PackageFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Package

    creator = factory.SubFactory(UserFactory)
    is_active = True
    is_flagged = False
    pkg_type = Package.APPLICATION
    name = factory.Sequence(lambda n: 'package-%s' % n)
