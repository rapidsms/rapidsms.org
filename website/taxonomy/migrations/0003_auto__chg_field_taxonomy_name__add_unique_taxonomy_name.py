# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Taxonomy.name'
        db.alter_column(u'taxonomy_taxonomy', 'name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80))
        # Adding unique constraint on 'Taxonomy', fields ['name']
        db.create_unique(u'taxonomy_taxonomy', ['name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Taxonomy', fields ['name']
        db.delete_unique(u'taxonomy_taxonomy', ['name'])


        # Changing field 'Taxonomy.name'
        db.alter_column(u'taxonomy_taxonomy', 'name', self.gf('django.db.models.fields.CharField')(max_length=40))

    models = {
        u'taxonomy.taxonomy': {
            'Meta': {'object_name': 'Taxonomy'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'})
        }
    }

    complete_apps = ['taxonomy']