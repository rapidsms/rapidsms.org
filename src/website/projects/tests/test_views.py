from django.core import mail
from django.urls import reverse

from website.datamaps.models import Country
from website.packages.tests.factories import PackageFactory
from website.tests.base import ViewTestMixin, WebsiteTestBase
from website.users.factories import UserFactory

from ..models import Project
from .factories import ProjectFactory

__all__ = ['TestProjectCreateView', 'ProjectReviewRequestTest',
           'ProjectDetailTest', ]


class ProjectDetailTest(ViewTestMixin, WebsiteTestBase):
    fixtures = ['countries.json']  # Loads initial django-datamaps data
    template_name = 'projects/project_detail.html'

    def setUp(self):
        self.project = ProjectFactory.create()
        self.url = self.project.get_absolute_url()

    def tearDown(self):
        self.client.logout()

    def test_get_authenticated(self):
        self.login_user(UserFactory.create())
        response = self._get(url=self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)

    def test_get_unauthenticated(self):
        response = self._get(url=self.url)
        self.assertTemplateUsed(response, self.template_name)

    def test_get_context_no_countries(self):
        """Tests for the output context when there are countries associated
        with current project"""
        response = self._get(url=self.url)
        self.assertNotIn('map_data', response.context)
        self.assertNotIn('scope', response.context)

    def test_get_context_countries(self):
        """Tests for the output context when there are countries associated
        with current project"""
        country = Country.objects.all()[0]
        self.project.countries.add(country)
        response = self._get(url=self.url)
        self.assertIn('map_data', response.context)
        self.assertIn('scope', response.context)


class TestProjectCreateView(ViewTestMixin, WebsiteTestBase):
    fixtures = ['countries.json']  # Loads initial django-datamaps data
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

    def setUp(self):
        self.user = UserFactory.create()
        self.project = ProjectFactory.create(creator=self.user,
                                             status=Project.DRAFT)
        self.url = reverse('project_review_request',
                           kwargs={'slug': self.project.slug})

    def tearDown(self):
        self.client.logout()

    def test_get_authenticated(self):
        """Test should raise a 405 since this method is not allowed."""
        self.login_user(self.user)
        response = self._get(url=self.url)
        self.assertEquals(response.status_code, 405)

    def test_post_unauthenticated(self):
        """Only logged users can access this view."""
        response = self._post(url=self.url)
        self.assertRedirectsToLogin(response)

    def test_post_authenticated(self):
        """Only logged users can request their project to be reviewed."""
        self.login_user(self.user)
        response = self._post(url=self.url)
        self.assertEqual(response.status_code, 301)
        updated_project = Project.objects.get(pk=self.project.id)
        self.assertEqual(updated_project.status, 'R')  # Status changed
        self.assertEqual(1, len(mail.outbox))
