# -*- coding: utf-8 -*-
from south.v2 import DataMigration

from django_countries.countries import COUNTRIES


class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        for country in COUNTRIES:
            # Country.name involves non-ascii characters and this can cause
            # south difficulties. The solution is to encode it as UTF-8
            country_name = country[1].encode("UTF-8")
            new_country = orm["projects.country"](name=country_name,
                                                  code=country[0])
            new_country.save()

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'projects.country': {
            'Meta': {'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['projects']
    symmetrical = True
