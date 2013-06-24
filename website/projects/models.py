from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify

from website.users.models import User


class Country(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name', ]
        verbose_name_plural = "Countries"


class Project(models.Model):
    creator = models.ForeignKey(User, related_name='created_projects',
            help_text='The creator of this content, who may or may not be its '
            'author.')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField()
    started = models.DateField('Project start date')

    countries = models.ManyToManyField(Country, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    challenges = models.TextField(blank=True, null=True)
    audience = models.TextField(blank=True, null=True)
    technologies = models.TextField(blank=True, null=True)
    metrics = models.TextField(blank=True, null=True)
    num_users = models.IntegerField(blank=True, null=True,
            help_text='Estimated number of users.')
    repository_url = models.URLField(blank=True, null=True, help_text='Link '
            'to the public code repository for this project.')

    class Meta:
        ordering = ['-updated']

    def __unicode__(self):
        return self.name

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
