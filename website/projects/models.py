from django.db import models
from django.template.defaultfilters import slugify


class Country(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name', ]
        verbose_name_plural = "Countries"


class Project(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField()
    countries = models.ManyToManyField(Country, blank=True, null=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('project-detail', (), {'project_id': self.pk})

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)
