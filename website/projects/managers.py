import random

from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet

from website.users.models import User


class ProjectQueryset(QuerySet):

    def in_countries(self, countries):
        """Returns QS of all projects in a given scope."""
        return self.filter(countries__in=countries)


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
        active = self.filter(status=self.model.PUBLISHED)
        if isinstance(user_or_package, User):
            user = user_or_package
            projects = active.filter(collaborators__in=[user, ])
        else:
            package = user_or_package
            projects = active.filter(packages__in=[package, ])
        return projects

    def get_feature_projects(self):
        """Returns a queryset off all feature projects"""
        return self.filter(feature=True)

    def get_feature_project(self):
        """Returns a random feature projects or None"""
        projects = self.get_feature_projects() or self.published()
        project = random.choice(projects) if projects else None
        return project
