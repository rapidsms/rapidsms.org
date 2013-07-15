from django.db import models
from django.db.models import Q


class ProjectManager(models.Manager):
    "Provides functionality to filter projects by current user."

    def get_drafts_for_user(self, user):
        """Return a queryset of drafts a user can edit"""
        drafts = self.filter(status=self.model.DRAFT)
        user_drafts = drafts.filter(
            Q(creator=user) | Q(collaborators__in=[user,])
        )
        return user_drafts
