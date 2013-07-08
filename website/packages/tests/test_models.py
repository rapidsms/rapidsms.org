import datetime
import json

from website.tests.base import WebsiteTestBase
from website.users.tests.factories import UserFactory

from ..models import Package, PYPI_DATE_FORMAT
from .base import MockPyPIRequest
from .factories import PackageFactory

__all__ = ['PackageModelTest']


class PackageModelTest(WebsiteTestBase):

    def test_update_from_pypi_200(self):
        package = PackageFactory.create()
        pypi_request = MockPyPIRequest(status_code=200, version='hello')
        updated = package.update_from_pypi(pypi_request)
        self.assertTrue(updated)
        self.assertEquals(package.version, 'hello')
        self.assertIsNotNone(package.pypi_updated)

    def test_update_from_pypi_200_release_date(self):
        package = PackageFactory.create()
        upload_time = datetime.datetime.strftime(datetime.datetime.now(),
            PYPI_DATE_FORMAT)
        pypi_request = MockPyPIRequest(status_code=200, upload_time=upload_time)
        updated = package.update_from_pypi(pypi_request)
        self.assertTrue(updated)
        release_date = datetime.datetime.strftime(package.release_date,
            PYPI_DATE_FORMAT)
        self.assertEqual(release_date, upload_time)

    def test_update_from_pypi_405(self):
        package = PackageFactory.create()
        pypi_request = MockPyPIRequest(status_code=405, version='hello')
        updated = package.update_from_pypi(pypi_request)
        self.assertFalse(updated)
        self.assertNotEquals(package.version, 'hello')
        self.assertIsNone(package.pypi_updated)

    def test_update_from_pypi_500(self):
        package = PackageFactory.create()
        pypi_request = MockPyPIRequest(status_code=500, version='hello')
        updated = package.update_from_pypi(pypi_request)
        self.assertFalse(updated)
        self.assertNotEquals(package.version, 'hello')
        self.assertIsNone(package.pypi_updated)

    def test_save_slug(self):
        user = UserFactory.create()
        package = Package(name='test-application', creator=user)
        self.assertEquals(package.slug, '')
        package.save()
        self.assertNotEquals(package.slug, '')

    def test_description(self):
        descr = 'Foo'
        data = json.dumps({'info': {'description': descr}})
        package = PackageFactory.create(pypi_json=data)
        self.assertIn(descr, package.description)
