from django.db import models


class Taxonomy(models.Model):
    name = models.CharField(max_length=80, unique=True)

    def __unicode__(self):
        return self.name
