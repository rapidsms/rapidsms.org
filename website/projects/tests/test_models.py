from website.tests.base import WebsiteTestBase
from website.users.tests.factories import UserFactory

from ..models import Country, Project
from .factories import ProjectFactory

__all__ = ['ProjectModelTest']


class ProjectModelTest(WebsiteTestBase):

    def test_unicode(self):
        project = ProjectFactory.create(name="rapidsms")
        self.assertEqual(project.name, project.__unicode__())

    def test_change_status(self):
        project = ProjectFactory.create(name="rapidsms", status='D')
        project.change_status('R')
        self.assertEqual(project.status, 'R')

    def test_display_countries_empty(self):
        project = ProjectFactory.create()
        self.assertEqual(project.display_countries(), '')

    def test_display_countries(self):
        us = Country.objects.get(code='USA')
        cn = Country.objects.get(code='CHN')
        ca = Country.objects.get(code='CAN')
        project = ProjectFactory.create()
        project.countries.add(us)
        self.assertEqual(project.display_countries(), us.name)
        project.countries.add(cn)
        formatted = '%s and %s' % (cn.name, us.name)
        self.assertEqual(project.display_countries(), formatted)
        project.countries.add(ca)
        formatted = '%s, %s, and %s' % (ca.name, cn.name, us.name)
        self.assertEqual(project.display_countries(), formatted)

    def test_get_model_name(self):
        project = ProjectFactory.create(name="rapidsms")
        self.assertEqual(project.get_model_name(), 'project')

    def test_get_delete_url(self):
        expected = '/projects/d/rapidsms/delete/'
        project = ProjectFactory.create(name="rapidsms")
        self.assertEqual(project.get_delete_url(), expected)

    def test_get_edit_url(self):
        expected = '/projects/d/rapidsms/edit/'
        project = ProjectFactory.create(name="rapidsms")
        self.assertEqual(project.get_edit_url(), expected)
