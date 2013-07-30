from datamaps.models import Scope

from website.projects.tests.factories import ProjectFactory
from website.tests.base import ViewTestMixin, WebsiteTestBase, BasicGetTest
from website.users.factories import UserFactory
from website.views import FacetedSearchCustomView

__all__ = ["HomePageViewTest", "AboutTest", "CommunityTest", "HelpTest",
           "FacetedSearchCustomViewTest", ]


class HomePageViewTest(ViewTestMixin, WebsiteTestBase):
    fixtures = ['countries.json']  # Loads initial django-datamaps data
    url_name = 'home'
    template_name = 'website/home.html'
    context_variables = ["feature_project", "map_data", "scope", ]

    def setUp(self):
        self.scope = Scope.objects.get(pk=1)
        self.country = self.scope.country_set.all()[0]
        self.second_scope = Scope.objects.get(pk=2)
        self.country = self.second_scope.country_set.all()[0]

    def tearDown(self):
        self.client.logout()

    def test_get_authenticated(self):
        """Logged in users can view the home page"""
        self.login_user(UserFactory.create())
        response = self._get()
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)

    def test_get_unauthenticated(self):
        """Unregistered users can view the home page"""
        response = self._get()
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)

    def test_empty_database(self):
        """Test that HomePage does not raises any errors when there is no
        data in the database. Other then the fixtures for countries."""
        response = self._get()
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)

    def test_context_varaibles(self):
        """Tests that the context variables that the template will get."""
        response = self._get()
        for var in self.context_variables:
            self.assertIn(var, response.context)

    def test_feature_project(self):
        """Tests that view returns a 200 when there is a feature project"""
        project = ProjectFactory.create(feature=True)  # Active feature project
        project.countries.add(self.country)
        response = self._get()
        self.assertEquals(response.status_code, 200)
        # Assert that the context variable equals the project we created.
        self.assertEqual(project, response.context['feature_project'])


class AboutTest(BasicGetTest):
    url_name = 'about'
    template_name = 'website/about.html'


class CommunityTest(BasicGetTest):
    url_name = 'community'
    template_name = 'website/community.html'


class HelpTest(BasicGetTest):
    url_name = 'help'
    template_name = 'website/help.html'


class FacetedSearchCustomViewTest(ViewTestMixin, WebsiteTestBase):

    def setUp(self):
        self.view = FacetedSearchCustomView

