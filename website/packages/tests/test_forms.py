import mock

from django.db import IntegrityError

from website.tests import factories
from website.tests.base import FormTestMixin, ModelFormTestMixin, WebsiteTestBase

from ..forms import PackageCreateEditForm, PackageFlagForm
from ..models import Package
from .base import MockPyPIRequest


__all__ = ['PackageCreateFormTest', 'PackageEditFormTest',
        'PackageFlagFormTest']


class PackageCreateFormTest(ModelFormTestMixin, WebsiteTestBase):
    form_class = PackageCreateEditForm

    def _get_form_data(self, **kwargs):
        data = {
            'pkg_type': Package.APPLICATION,
            'name': 'test-application',
        }
        data.update(kwargs)
        return data

    def _validate_form(self, form, mock_status_code=200):
        """Wrapper around form validation, to mock the PyPI request."""
        with mock.patch.object(Package, '_get_pypi_request') as mock_get:
            mock_get.return_value = MockPyPIRequest(status_code=mock_status_code)
            return form.is_valid()

    def test_fields(self):
        """Four fields should be included when there is no instance."""
        form = self._get_form(data=None)
        self.assertEquals(len(form.fields), 4)
        self.assertTrue('pkg_type' in form.fields)
        self.assertTrue('name' in form.fields)
        self.assertTrue('tests_url' in form.fields)
        self.assertTrue('repo_url' in form.fields)

    def test_pypi_500(self):
        """
        name field should raise ValidationError if PyPI returns a 500 error.
        """
        form = self._get_form()
        self.assertFalse(self._validate_form(form, mock_status_code=500))
        self.assertTrue('name' in form.errors)

    def test_pypi_404(self):
        """
        name field should raise ValidationError if PyPI returns a 404 error.
        """
        form = self._get_form()
        self.assertFalse(self._validate_form(form, mock_status_code=404))
        self.assertTrue('name' in form.errors)

    def test_no_user(self):
        """User object must be set on the instance before it can be saved."""
        form = self._get_form()
        self.assertTrue(self._validate_form(form), form.errors)
        self.assertRaises(IntegrityError, form.save)

    def test_no_name(self):
        """name field should be required."""
        data = self._get_form_data(name='')
        form = self._get_form(data=data)
        self.assertFalse(self._validate_form(form))
        self.assertTrue('name' in form.errors)

    def test_no_pkg_type(self):
        """pkg_type field should be required."""
        data = self._get_form_data(pkg_type='')
        form = self._get_form(data=data)
        self.assertFalse(self._validate_form(form))
        self.assertTrue('pkg_type' in form.errors)

    def test_no_tests_url(self):
        """tests_url field should not be required."""
        data = self._get_form_data(tests_url='')
        form = self._get_form(data=data)
        self.assertTrue(self._validate_form(form), form.errors)

    def test_no_repo_url(self):
        """repo_url field should not be required."""
        data = self._get_form_data(repo_url='')
        form = self._get_form(data=data)
        self.assertTrue(self._validate_form(form), form.errors)

    def test_valid(self):
        form = self._get_form()
        self.assertTrue(self._validate_form(form), form.errors)
        form.instance.creator = factories.UserFactory.create()
        package = form.save()
        self.assertEquals(package.pkg_type, Package.APPLICATION)
        self.assertEquals(package.name, 'test-application')


class PackageEditFormTest(ModelFormTestMixin, WebsiteTestBase):
    form_class = PackageCreateEditForm

    def setUp(self):
        self.package = factories.PackageFactory.create()

    def _get_form_instance(self):
        return self.package

    def _get_form_data(self, **kwargs):
        data = {
            'repo_url': u'http://example.com/',
            'tests_url': u'http://example.com/',
        }
        data.update(kwargs)
        return data

    def test_fields(self):
        """Edit field field should not have name or pkg_type fields."""
        form = self._get_form(data=None)
        self.assertEquals(len(form.fields), 2)
        self.assertTrue('tests_url' in form.fields)
        self.assertTrue('repo_url' in form.fields)

    def test_no_tests_url(self):
        """tests_url field should not be required."""
        data = self._get_form_data(test_url='')
        form = self._get_form(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_no_repo_url(self):
        """repo_url field should not be required."""
        data = self._get_form_data(repo_url='')
        form = self._get_form(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_valid(self):
        form = self._get_form()
        self.assertTrue(form.is_valid(), form.errors)
        package = form.save()
        self.assertEquals(package.tests_url, u'http://example.com/')
        self.assertEquals(package.repo_url, u'http://example.com/')


class PackageFlagFormTest(FormTestMixin, WebsiteTestBase):
    form_class = PackageFlagForm

    def _get_form_data(self, **kwargs):
        data = {
            'reason': 'hello',
        }
        data.update(kwargs)
        return data

    def test_no_reason(self):
        """reason field should be required."""
        form = self._get_form(data={'reason': ''})
        self.assertFalse(form.is_valid())
        self.assertTrue('reason' in form.errors)

    def test_valid(self):
        form = self._get_form()
        self.assertTrue(form.is_valid())
