import datetime
import json

from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone

import requests
from docutils.core import publish_parts

from website.apps.taxonomy.models import Taxonomy
from website.apps.users.models import User

from .managers import PackageManager

PYPI_BADGE_URL = 'https://pypip.in/v/{0}/badge.png'
PYPI_JSON_API = 'http://pypi.python.org/pypi/{0}/json'
PYPI_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'


class Package(models.Model):
    APPLICATION = 'A'
    BACKEND = 'B'
    LIBRARY = 'L'
    ROUTER = 'R'
    PACKAGE_TYPES = {
        APPLICATION: 'Application',
        BACKEND: 'Backend',
        LIBRARY: 'Library',
        ROUTER: 'Router',
    }

    # Internal metadata, not displayed anywhere.
    creator = models.ForeignKey(User, related_name='created_packages', on_delete=models.CASCADE,
                                help_text="The creator of this content, who may or may not be its author.")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    pypi_updated = models.DateTimeField('PyPI Updated', null=True, blank=True)
    is_active = models.BooleanField('Active', default=True)
    is_flagged = models.BooleanField('Flagged', default=False)

    # Required data. Once this information has been entered, it cannot be
    # edited.
    pkg_type = models.CharField('Package Type', max_length=1, choices=PACKAGE_TYPES.items(), default=APPLICATION)
    name = models.CharField(max_length=255, unique=True, help_text="The name of the package on PyPI.")
    slug = models.SlugField()  # Derived from name.
    tags = models.ManyToManyField(Taxonomy, related_name="packages", verbose_name="Taxonomy")

    # Other reference URLs for the package are optional.
    tests_url = models.URLField(
        'CI/Tests', null=True, blank=True,
        help_text="Link to the package's public CI server, e.g. <a href='https://travis-ci.org/rapidsms/rapidsms'>"
                  "https://travis-ci.org/rapidsms/rapidsms</a>.")
    repo_url = models.URLField(
        'Source Code', null=True, blank=True,
        help_text="The package's source code repository, e.g. <a href='https://github.com/rapidsms/rapidsms'>"
                  "https://github.com/rapidsms/rapidsms</a>.")

    # We'll retrieve the package data from PyPI, and cache it on the model.
    # Also storing a few fields on the model to make them easier to index by
    # and search.
    pypi_json = models.TextField(null=True, blank=True)
    author_name = models.CharField(max_length=255, null=True, blank=True)
    author_email = models.EmailField(null=True, blank=True)
    maintainer_name = models.CharField(max_length=255, null=True, blank=True)
    maintainer_email = models.EmailField(null=True, blank=True)
    version = models.CharField(max_length=32, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    release_date = models.DateTimeField(null=True, blank=True)
    license = models.CharField(max_length=128, null=True, blank=True)
    docs_url = models.URLField(
        'Documentation', null=True, blank=True,
        help_text="Where the package's documentation is hosted, e.g. "
        "<a href='http://rapidsms.readthedocs.org/'>"
        "http://rapidsms.readthedocs.org</a>.")
    home_url = models.URLField(
        'Home Page', null=True, blank=True,
        help_text="The project's home page, e.g. <a href='http://rapidsms.org'>http://rapidsms.org</a>.")
    objects = PackageManager()

    class Meta:
        ordering = ['-release_date', '-updated']

    def __str__(self):
        return self.name

    def _get_pypi_request(self):
        return requests.get(self.get_pypi_json_url())

    @property
    def description(self):
        """
        This PyPI-derived field is not cached on the model, as we do not need
        to filter or order by it.
        """
        if self.pypi_json:
            data = json.loads(self.pypi_json)
            if data:
                desc = data['info']['description']
                return publish_parts(desc, writer_name='html')['html_body']

    def get_absolute_url(self):
        return reverse('package_detail', args=(self.slug,))

    def get_edit_url(self):
        return reverse('package_edit', args=(self.slug,))

    def get_flag_url(self):
        return reverse('package_flag', args=(self.slug,))

    def get_pypi_badge_url(self):
        return PYPI_BADGE_URL.format(self.name)

    def get_pypi_json_url(self):
        return PYPI_JSON_API.format(self.name)

    def get_refresh_url(self):
        return reverse('package_refresh', args=(self.slug,))

    def get_model_name(self):
        return self._meta.verbose_name

    def save(self, *args, **kwargs):
        # Set the slug on a newly-created package.
        if not self.id:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def update_from_pypi(self, request=None):
        """
        Retrieve data from PyPI, and if successful with that update the
        PyPI-derived fields on this model. Optionally uses an existing request
        to populate data.

        Returns a boolean indicating if the update is successful. Does not save
        the model.
        """
        req = request or self._get_pypi_request()
        if req.status_code != 200:
            return False

        data = req.json()
        self.pypi_json = json.dumps(data)
        if self.pypi_json:
            self.maintainer_name = data['info']['maintainer']
            self.maintainer_email = data['info']['maintainer_email']
            self.author_name = data['info']['author']
            self.author_email = data['info']['author_email']
            self.version = data['info']['version']
            self.summary = data['info']['summary']
            self.docs_url = data['info']['docs_url']
            self.home_url = data['info']['home_page']
            self.license = data['info']['license']
            d = data['urls'][0]['upload_time']
            if d:
                self.release_date = datetime.datetime.strptime(d, PYPI_DATE_FORMAT)
        self.pypi_updated = timezone.now()

        return True
