from django.db import models


class PackageManager(models.Manager):
    """Model manager for Package model."""

    def active_packages(self):
        return self.filter(is_active=True)
