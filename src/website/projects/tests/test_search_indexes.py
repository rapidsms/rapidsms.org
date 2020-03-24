from django.test import TestCase

from ..models import Project
from ..search_indexes import ProjectIndex

__all__ = ['ProjectIndexTest', ]


class ProjectIndexTest(TestCase):

    def setUp(self):
        self.index = ProjectIndex()

    def test_get_model(self):
        self.assertEqual(self.index.get_model(), Project)
