from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify

from taggit.managers import TaggableManager

from .managers import ProjectManager
from website.packages.models import Package
from website.users.models import User


class Country(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['name', ]
        verbose_name_plural = "Countries"
        unique_together = (("code", "name"),)

    def __unicode__(self):
        return self.name


class Project(models.Model):
    DRAFT = 'D'
    NEEDS_REVIEW = 'R'
    PUBLISHED = 'P'
    DENIED = 'N'
    STATUS = (
        (DRAFT, 'Draft'),
        (NEEDS_REVIEW, 'Needs Review'),
        (PUBLISHED, 'Published'),
        (DENIED, 'Denied'),
    )

    creator = models.ForeignKey(User, related_name='created_projects',
            help_text="The creator of this content, who may or may not be its "
            "author.")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(default=DRAFT, max_length=1, choices=STATUS)
    is_active = models.BooleanField('Active', default=False)

    collaborators = models.ManyToManyField(User, related_name='projects',
            help_text="Users who have permission to edit this project.")

    # Required data.
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField()
    description = models.TextField()

    # Optional information.
    started = models.DateField('Project start date', null=True, blank=True)
    countries = models.ManyToManyField(Country, blank=True, null=True)
    challenges = models.TextField(blank=True, null=True)
    audience = models.TextField(blank=True, null=True)
    technologies = models.TextField('Key technologies', blank=True, null=True)
    metrics = models.TextField(blank=True, null=True)
    num_users = models.IntegerField('Number of users', blank=True, null=True,
            help_text='Estimated number of users, a whole number.')
    repository_url = models.URLField(blank=True, null=True, help_text='Link '
            'to the public code repository for this project.')
    tags = TaggableManager(verbose_name="Taxonomy")
    packages = models.ManyToManyField(Package, blank=True, null=True)
    script = models.TextField(help_text="JS/JSON blob", blank=True)
    objects = ProjectManager()

    class Meta:
        ordering = ['-updated']

    def __unicode__(self):
        return self.name

    def can_edit(self, user):
        "Check if a users has rights to edit this instance"
        if user == self.creator or user in self.collaborators.all():
            return True

    def change_status(self, new_status, send_notification=False):
        """Change current status of instance"""
        self.status = new_status
        self.save(update_fields=['status', ])
        return True

    def display_countries(self):
        """Display countries as a comma-separated list."""
        total = self.countries.count()
        result = ''
        for index, country in enumerate(self.countries.all(), 1):
            if index == total and index != 1:
                result += 'and '
            result += str(country)
            if index != total:
                result += ', ' if total > 2 else ' '
        return result

    def get_absolute_url(self):
        return reverse('project_detail', args=(self.slug,))

    def get_delete_url(self):
        return reverse('project_delete', args=(self.slug,))

    def get_edit_url(self):
        return reverse('project_edit', args=(self.slug,))

    def get_model_name(self):
        return self._meta.verbose_name

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)
