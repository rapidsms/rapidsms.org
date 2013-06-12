import requests

from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify

from website.users.models import User


class Package(models.Model):
    APPLICATION = 'A'
    BACKEND = 'B'
    ROUTER = 'R'
    PACKAGE_TYPES = {
        APPLICATION: 'Application',
        BACKEND: 'Backend',
        ROUTER: 'Router',
    }

    # Internal metadata.
    creator = models.ForeignKey(User, help_text='The creator of this content, '
            'who may or may not be the author of the package.')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField()

    # Required descriptors.
    name = models.CharField(max_length=255, unique=True)
    pkg_type = models.CharField('Package Type', max_length=1,
            choices=PACKAGE_TYPES.items(), default=APPLICATION)
    pypi_url = models.URLField('PyPI URL')
    has_tests = models.BooleanField(help_text="Are there tests?")
    has_docs = models.BooleanField(help_text="Are there docs?")

    # Optional descriptors.
    description = models.TextField(null=True, blank=True)
    repository_url = models.URLField(null=True, blank=True, help_text='Link '
            'to the public code repository for this project.')

    class Meta:
        ordering = ['-updated']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('package_detail', args=(self.slug,))

    def get_edit_url(self):
        return reverse('package_edit', args=(self.slug,))

    def get_pypi_json(self):
        try:
            r = requests.get('{0}/json'.format(self.pypi_url.rstrip('/')))
            return r.json()
        except:
            return None

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)
        super(Package, self).save(*args, **kwargs)
