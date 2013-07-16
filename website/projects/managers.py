from django.db import models
from django.db.models import Q

from website.users.models import User


class ProjectManager(models.Manager):
    "Provides functionality to filter projects by current user."

    def get_drafts_for_user(self, user):
        """Returns a queryset of drafts a user can edit"""
        drafts = self.filter(status=self.model.DRAFT)
        user_drafts = drafts.filter(
            Q(creator=user) | Q(collaborators__in=[user, ])
        )
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
