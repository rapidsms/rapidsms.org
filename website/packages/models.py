import datetime
from docutils.core import publish_parts
import json
import requests

from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify

from website.users.models import User


PYPI_JSON_API = 'http://pypi.python.org/pypi/{0}/json'
PYPI_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'


class Package(models.Model):
    APPLICATION = 'A'
    BACKEND = 'B'
    ROUTER = 'R'
    PACKAGE_TYPES = {
        APPLICATION: 'Application',
        BACKEND: 'Backend',
        ROUTER: 'Router',
    }

    # Internal metadata, not displayed anywhere.
    creator = models.ForeignKey(User, related_name='created_packages',
            help_text="The creator of this content, who may or may not be its "
            "author.")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    pypi_updated = models.DateTimeField(null=True, blank=True)

    # Required data. Once this information has been entered, it cannot be
    # edited.
    pkg_type = models.CharField('Package Type', max_length=1,
            choices=PACKAGE_TYPES.items(), default=APPLICATION)
    name = models.CharField(max_length=255, unique=True, help_text="The name "
            "of the package on PyPI.")
    slug = models.SlugField()  # Derived from name.

    # Other reference URLs for the package are optional.
    docs_url = models.URLField('Documentation', null=True, blank=True,
            help_text="Where the package's documentation is hosted, e.g. "
            "<a href='http://rapidsms.readthedocs.org/'>"
            "http://rapidsms.readthedocs.org</a>.")
    tests_url = models.URLField('CI/Tests', null=True, blank=True,
            help_text="Link to the package's public CI server, e.g. "
            "<a href='https://travis-ci.org/rapidsms/rapidsms'>"
            "https://travis-ci.org/rapidsms/rapidsms</a>.")
    repo_url = models.URLField('Source Code', null=True, blank=True,
            help_text="The package's source code repository, e.g. "
            "<a href='https://github.com/rapidsms/rapidsms'>"
            "https://github.com/rapidsms/rapidsms</a>.")
    home_url = models.URLField('Home Page', null=True, blank=True,
            help_text="The project's home page, e.g. "
            "<a href='http://rapidsms.org'>http://rapidsms.org</a>.")

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

    class Meta:
        ordering = ['-release_date', '-updated']

    def __unicode__(self):
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

    def get_pypi_json_url(self):
        return PYPI_JSON_API.format(self.name)

    def get_model_name(self):
        return self._meta.verbose_name

    def save(self, *args, **kwargs):
        # Set the slug on a newly-created package.
        if not self.id:
            self.slug = slugify(self.name)
        super(Package, self).save(*args, **kwargs)

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

        self.pypi_json = json.dumps(req.json())
        if self.pypi_json:
            data = json.loads(self.pypi_json)
            if data:
                self.maintainer_name = data['info']['maintainer']
                self.maintainer_email = data['info']['maintainer_email']
                self.author_name = data['info']['author']
                self.author_email = data['info']['author_email']
                self.version = data['info']['version']
                self.summary = data['info']['summary']

                d = data['urls'][0]['upload_time']
                if d:
                    self.release_date = datetime.datetime.strptime(d, PYPI_DATE_FORMAT)
        self.pypi_updated = datetime.datetime.now()

        return True
