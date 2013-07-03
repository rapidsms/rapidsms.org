from website.tests import factories
from website.tests.base import WebsiteTestBase

from ..models import Package
from .base import MockPyPIRequest


__all__ = ['PackageModelTest']


class PackageModelTest(WebsiteTestBase):

    def test_update_from_pypi_200(self):
        package = factories.PackageFactory.create()
        pypi_request = MockPyPIRequest(status_code=200, version='hello')
        updated = package.update_from_pypi(pypi_request)
        self.assertTrue(updated)
        self.assertEquals(package.version, 'hello')
        self.assertIsNotNone(package.pypi_updated)

    def test_update_from_pypi_405(self):
        package = factories.PackageFactory.create()
        pypi_request = MockPyPIRequest(status_code=405, version='hello')
        updated = package.update_from_pypi(pypi_request)
        self.assertFalse(updated)
        self.assertNotEquals(package.version, 'hello')
        self.assertIsNone(package.pypi_updated)

    def test_update_from_pypi_500(self):
        package = factories.PackageFactory.create()
        pypi_request = MockPyPIRequest(status_code=500, version='hello')
        updated = package.update_from_pypi(pypi_request)
        self.assertFalse(updated)
        self.assertNotEquals(package.version, 'hello')
        self.assertIsNone(package.pypi_updated)

    def test_save_slug(self):
        user = factories.UserFactory.create()
        package = Package(name='test-application', creator=user)
        self.assertEquals(package.slug, '')
        package.save()
        self.assertNotEquals(package.slug, '')
