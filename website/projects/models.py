import random

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string

from .managers import ProjectManager
from website.tasks import send_email
from website.packages.models import Package
from website.taxonomy.models import Taxonomy
from website.users.models import User


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
    NUM_USERS = (
        (1, 'Under 100'),
        (2, '100 - 1,000'),
        (3, '1,000 - 5,000'),
        (4, '5,000 - 100,000'),
        (5, '100,000+')
    )

    creator = models.ForeignKey(User, related_name='created_projects',
            help_text="The creator of this content, who may or may not be its "
            "author.")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(default=DRAFT, max_length=1, choices=STATUS)
    feature = models.BooleanField('Featured on Homepage', default=False,
            help_text="Check box to make this project the featured project.")

    collaborators = models.ManyToManyField(User, related_name='projects',
            help_text="Users who have permission to edit this project.")

    # Required data.
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField()
    description = models.TextField()

    # Optional information.
    started = models.DateField('Project start date', null=True, blank=True,
        help_text='mm/dd/yyyy')
    countries = models.ManyToManyField('datamaps.Country', blank=True, null=True)
    challenges = models.TextField(blank=True, null=True)
    audience = models.TextField(blank=True, null=True)
    technologies = models.TextField('Key technologies', blank=True, null=True)
    metrics = models.TextField(blank=True, null=True)
    num_users = models.IntegerField('Number of users', blank=True, null=True,
            choices=NUM_USERS, help_text='Choose one of the options available.',
            default=1)
    repository_url = models.URLField(blank=True, null=True, help_text='Link '
            'to the public code repository for this project.')
    tags = models.ManyToManyField(Taxonomy, related_name="projects",
        verbose_name="Taxonomy")
    packages = models.ManyToManyField(Package, blank=True, null=True)
    script = models.TextField(help_text="JS/JSON blob", blank=True)
    project_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='logos', blank=True, null=True,
        help_text="Project Logo")
    files = models.FileField('Attach a file', upload_to='files', blank=True,
        null=True)
    objects = ProjectManager()

    class Meta:
        ordering = ['-updated']

    def __unicode__(self):
        return self.name

    def can_edit(self, user):
        "Check if a users has rights to edit this instance"
        if user == self.creator or user in self.collaborators.all():
            return True

    def change_status(self, status):
        """Change current status of instance and determines whether or not
        this instance is active"""
        # Sends email only when a change in status occurs
        recipients = 'admins' if status == self.NEEDS_REVIEW else 'users'
        if not self.status == status:
            self.notify(recipients, status)
        #set new status and save changes
        self.status = status
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

    def _get_email_content(self, status):
        "Loads and renders subject and body contents for email notifications."
        site = Site.objects.get(pk=1)
        context = {'object': self, 'site': site}
        if status == self.NEEDS_REVIEW:
            subject = render_to_string(
                'projects/emails/project_needs_review_subject.txt',
                context
            )
            body = render_to_string(
                'projects/emails/project_needs_review_body.txt',
                context
            )
        elif status == self.PUBLISHED:
            subject = render_to_string(
                'projects/emails/project_published_subject.txt',
                context
            )
            body = render_to_string(
                'projects/emails/project_published_subject.txt',
                context
            )
        else:  # Last option: status == self.DENIED
            subject = render_to_string(
                'projects/emails/project_denied_subject.txt',
                context
            )
            body = render_to_string(
                'projects/emails/project_denied_subject.txt',
                context
            )
        return subject, body

    def _get_to_addresses(self, to):
        """Returns a list of email addresses.

        args:
        to -> takes two possible values ('users', 'admins')
        """
        if to == 'users':
            return [self.creator.email, ]
        else:
            return settings.PROJECT_EMAIL_ALERTS

    def get_absolute_url(self):
        return reverse('project_detail', args=(self.slug,))

    def get_delete_url(self):
        return reverse('project_delete', args=(self.slug,))

    def get_edit_url(self):
        return reverse('project_edit', args=(self.slug,))

    def get_model_name(self):
        return self._meta.verbose_name

    def get_map_data(self, country):
        return {'name': self.name,
                'fillKey': 'project',
                'url': self.get_absolute_url(),
                'description': self.short_description,
                'country': country.name
                }

    def get_bubble_data(self, country):
        """Returns a dict with info for bubbles drawing.

        At a bare minimum it should contain the following keys:
        radius, latitude and longitude. You can pass more keys
        and they will be available for you to use on your map's
        popup template.

        """
        radius_options = [5, 8, 11, 14, 17]  # Radius selected a random
        return {'name': self.name,
                'radius': random.choice(radius_options),
                'fillKey': 'project',
                'url': self.get_absolute_url(),
                'description': self.short_description,
                'latitude': country.lat,
                'longitude': country.lon,
                'country': country.name
                }

    def notify(self, to, status):
        """Sends email notification to users or admins.

        args:
        to -> takes to possible values "users" or "admins"
        status -> takes the status that needs to be notified.

        eg.
        notify('admins', 'Needs_Review') #send email alerting admins that
        a project needs review.
        """
        # import pdb; pdb.set_trace()
        subject, body = self._get_email_content(status)
        to = self._get_to_addresses(to)
        send_email.delay(subject, body, settings.DEFAULT_FROM_EMAIL, to)

    def save(self, *args, **kwargs):
        """Saves instance slug field"""
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)
        if self.feature:
            self.__class__.objects.get_feature_projects().update(feature=False)
        super(Project, self).save(*args, **kwargs)

    @property
    def short_description(self):
        description = self.description
        lenght = len(description)
        if lenght <= 120:
            return description
        return description[0:119]
