import requests

from django.db import models
from django.template.defaultfilters import slugify


class Package(models.Model):
    APPLICATION = 0
    BACKEND = 1
    ROUTER = 2
    PACKAGE_TYPE_CHOICES = {
        APPLICATION: 'Application',
        BACKEND: 'Backend',
        ROUTER: 'Router',
    }
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    slug = models.SlugField()
    pkg_type = models.SmallIntegerField(choices=PACKAGE_TYPE_CHOICES.items(),
                                        default=APPLICATION)
    pypi_url = models.URLField()
    has_tests = models.BooleanField(help_text="Does the package have tests?")
    has_docs = models.BooleanField(help_text="Does the package have documentation?")

    def __unicode__(self):
        return self.name

    def get_pypi_json(self):
        try:
            r = requests.get('{0}/json'.format(self.pypi_url.rstrip('/')))
            return r.json()
        except:
            return None

    @models.permalink
    def get_absolute_url(self):
        return ('project-detail', (), {'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)
        super(Package, self).save(*args, **kwargs)
