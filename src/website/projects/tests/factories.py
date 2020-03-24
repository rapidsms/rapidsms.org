import factory
from website.users.factories import UserFactory

from ..models import Project

__all__ = ['ProjectFactory']


class ProjectFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Project

    creator = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: 'project-%s' % n)
    feature = False
    status = Project.PUBLISHED
