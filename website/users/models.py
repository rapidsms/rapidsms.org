from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from website.projects.models import Country


class User(AbstractUser):
    INDIVIDUAL = 'I'
    ORGANIZATION = 'O'
    USER_TYPES = {
        INDIVIDUAL: 'Individual',
        ORGANIZATION: 'Organization',
    }
    user_type = models.CharField(max_length=1, choices=USER_TYPES.items())

    location = models.CharField(max_length=255, null=True, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True)

    website_url = models.URLField(null=True, blank=True)
    github_url = models.URLField(null=True, blank=True)
    for_hire = models.BooleanField(default=False)

    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
        return super(User, self).get_full_name() or self.username
