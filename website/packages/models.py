import requests

from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify


class Package(models.Model):
    APPLICATION = 'A'
    BACKEND = 'B'
    ROUTER = 'R'
    PACKAGE_TYPES = {
        APPLICATION: 'Application',
        BACKEND: 'Backend',
        ROUTER: 'Router',
    }

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    slug = models.SlugField()
    pkg_type = models.CharField('Package Type', max_length=1,
            choices=PACKAGE_TYPES.items(), default=APPLICATION)
    pypi_url = models.URLField('PyPI URL')
    has_tests = models.BooleanField(help_text="Are there tests?")
    has_docs = models.BooleanField(help_text="Are there docs?")

    def __unicode__(self):
        return self.name

    def get_pypi_json(self):
        try:
            r = requests.get('{0}/json'.format(self.pypi_url.rstrip('/')))
            return r.json()
        except:
            return None

    def get_absolute_url(self):
        return reverse('package_detail', args=(self.slug,))

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)
        super(Package, self).save(*args, **kwargs)
