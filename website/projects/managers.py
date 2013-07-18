import random

from django.db import models
from django.db.models import Q

from website.users.models import User


class ProjectManager(models.Manager):

    def get_drafts_for_user(self, user):
        """Returns a queryset of drafts a user can edit"""
        drafts = self.filter(status=self.model.DRAFT)
        user_drafts = drafts.filter(
            Q(creator=user) | Q(collaborators__in=[user, ])
        ).distinct()
        return user_drafts

    def get_related_projects(self, user_or_package):
        """"Returns a queryset with all projects that are related."""
        active = self.filter(is_active=True)
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
        projects = self.get_feature_projects()
        if projects:
            project = random.choice(projects)
            return project
        return None