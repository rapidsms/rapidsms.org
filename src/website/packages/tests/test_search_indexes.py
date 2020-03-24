from django.test import TestCase

from ..models import Package
from ..search_indexes import PackageIndex
from .factories import PackageFactory

__all__ = ['PackageIndexTest', ]


class PackageIndexTest(TestCase):

    def setUp(self):
        self.index = PackageIndex()

    def test_get_model(self):
        self.assertEqual(self.index.get_model(), Package)

    def test_prepare_pkg_type(self):
        package = PackageFactory.create(pkg_type="A")
        expected = package.get_pkg_type_display()
        output = self.index.prepare_pkg_type(package)
        self.assertEqual(output, expected)
