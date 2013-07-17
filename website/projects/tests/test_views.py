from website.packages.tests.factories import PackageFactory
from website.tests.base import ViewTestMixin, WebsiteTestBase
from website.users.tests.factories import UserFactory

from ..models import Country, Project
from .factories import ProjectFactory

__all__ = ['TestProjectCreateView']


class TestProjectCreateView(ViewTestMixin, WebsiteTestBase):
    url_name = 'project_create'
    template_name = 'projects/project_form.html'

    def test_get_authenticated(self):
        self.login_user(UserFactory.create())
        response = self._get()
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertFalse('object' in response.context)

    def test_get_unauthenticated(self):
        self.client.logout()
        response = self._get()
        self.assertRedirectsToLogin(response)

    def test_post_unauthenticated(self):
        self.client.logout()
        response = self._post()
        self.assertRedirectsToLogin(response)

    def test_create(self):
        self.login_user(UserFactory.create())
        us = Country.objects.get(code='USA')
        pkg = PackageFactory.create()
        response = self._post(data={
            'name': 'test-project',
            'description': 'Description',
            'tags': 'Tag',
            'num_users': 1,
            'countries_1': [us.pk],
            'packages_1': [pkg.pk],

        })
        self.assertEquals(Project.objects.count(), 1)
        project = Project.objects.get()
        self.assertEqual(pkg, project.packages.all()[0])
        self.assertEqual(us, project.countries.all()[0])
        self.assertRedirectsNoFollow(response, project.get_absolute_url())

    def test_create_invalid(self):
        self.login_user(UserFactory.create())
        response = self._post(data={
            'name': 'test-project',
        })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertFalse(response.context['form'].is_valid())


class ProjectReviewRequestTest(ViewTestMixin, WebsiteTestBase):
    pass
