from website.tests.base import WebsiteTestBase
from website.users.tests.factories import UserFactory

from ..models import Country, Project
from .factories import ProjectFactory

__all__ = ['ProjectModelTest']


class ProjectModelTest(WebsiteTestBase):

    def test_display_countries_empty(self):
        project = ProjectFactory.create()
        self.assertEqual(project.display_countries(), '')

    def test_display_countries(self):
        us = Country.objects.get(code='US')
        cn = Country.objects.get(code='CN')
        ca = Country.objects.get(code='CA')
        project = ProjectFactory.create()
        project.countries.add(us)
        self.assertEqual(project.display_countries(), us.name)
        project.countries.add(cn)
        formatted = '%s and %s' % (cn.name, us.name)
        self.assertEqual(project.display_countries(), formatted)
        project.countries.add(ca)
        formatted = '%s, %s, and %s' % (ca.name, cn.name, us.name)
        self.assertEqual(project.display_countries(), formatted)
