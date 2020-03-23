from django.db import models
from .tasks import update_packages


class PackageManager(models.Manager):
    """Model manager for Package model."""

    def active_packages(self):
        return self.filter(is_active=True)
