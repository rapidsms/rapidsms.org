import factory

from website.apps.users.factories import UserFactory

from ..models import Project

__all__ = ['ProjectFactory']


class ProjectFactory(factory.DjangoModelFactory):

    creator = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: 'project-%s' % n)
    feature = False
    status = Project.PUBLISHED

    class Meta:
        model = Project
