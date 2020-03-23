import random

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from website.packages.models import Package
from website.users.models import User


class ProjectQueryset(QuerySet):

    def filter_by_scope(self, scope=None):
        """Returns a QS all projects in a given scope."""
        return self.filter(countries__scope=scope).distinct()

    def get_random_sample(self):
        """Returns a random sample Generator.

        The number of elements in the Generator is defined by the
        setting, 'DISPLAY_NUM_PROJECTS', and defaults to the length
        of the queryset.
        """
        length = self.count()
        sample_size = getattr(settings, 'DISPLAY_NUM_PROJECTS', length)
        if length < sample_size:
            sample_size = length
        return [self[index] for index in random.sample(xrange(length),
                                                       sample_size)]


class ProjectManager(models.Manager):

    def get_query_set(self):
        return ProjectQueryset(self.model)

    def get_drafts_for_user(self, user):
        """Returns a queryset of drafts a user can edit"""
        drafts = self.filter(status=self.model.DRAFT)
        user_drafts = drafts.filter(
            Q(creator=user) | Q(collaborators__in=[user, ])
        ).distinct()
        return user_drafts

    def published(self):
        """Return QS of published projects"""
        return self.filter(status=self.model.PUBLISHED)

    def get_related_projects(self, user_or_package):
        """"Returns a queryset with all projects that are related."""
        active = self.published()
        if isinstance(user_or_package, User):
            user = user_or_package
            projects = active.filter(collaborators__in=[user, ])
        elif isinstance(user_or_package, Package):
            package = user_or_package
            projects = active.filter(packages__in=[package, ])
        else:
            raise Exception("This method only accepts an user or a packages as arguments.")
        return projects

    def get_feature_projects(self):
        return self.filter(feature=True)

    def get_feature_project(self):
        """Returns a random feature project or None"""
        try:
            project = self.get(feature=True)
        except self.model.DoesNotExist:
            project = None
        return project
