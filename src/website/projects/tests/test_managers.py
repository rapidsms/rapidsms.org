from django.test import TestCase

from ..models import Project

__all__ = ["ProjectQuerysetTest", "ProjectManagerTest"]


class ProjectQuerysetTest(TestCase):

    def test_get_ramdom_sample_empty_qs(self):
        projects = Project.objects.all()  # Empty queryset
        random_projects = projects.get_random_sample()
        self.assertEqual([], random_projects)


class ProjectManagerTest(TestCase):
    pass
